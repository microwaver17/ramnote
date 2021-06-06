import axios, { AxiosResponse } from 'axios'

import { config } from './config'
import { Note, Tag, ServerResponse } from './models'

const api = config.apiRoot

export const dao = Object.freeze({
    getTags(): Promise<Tag[]> {
        return new Promise((resolve, reject) => {
            axios.get(api + 'tags')
                .then(res => {
                    const tags: Tag[] = [];
                    (res.data as Array<any>).forEach(tag => {
                        tags.push(new Tag(tag['id'], tag['name']))
                    })
                    resolve(tags)

                }).catch(err => {
                    reject(new ServerResponse(err.response.data.result))
                })
        })
    },

    getNotes(): Promise<Note[]> {
        return new Promise((resolve, reject) => {
            axios.get(api + 'notes')
                .then(res => {
                    const notes: Note[] = [];
                    (res.data as Array<any>).forEach(note => {
                        // DB格納形式とJS格納形式の変換
                        const date = new Date(note['date'])     // DB側ではUNIX時間で格納しているので変換する
                        let tags: Array<Tag> = []
                        if (note['tags'] != '') {
                            tags = (note['tags'].split(',') as Array<string>).map(tag => new Tag(null, tag))
                        }
                        notes.push(new Note(note['id'], note['title'], note['body'], date, tags))
                    })
                    resolve(notes)

                }).catch(err => {
                    reject(new ServerResponse(err.response.data.result))
                })
        })
    },

    createNotes(note: Note): Promise<ServerResponse> {
        return new Promise((resolve, reject) => {
            const sendData: any = Object.assign({}, note)
            sendData.date = sendData.date.getTime()     // DB側ではUNIX時間で格納しているので変換する
            sendData.tags = sendData.tags.join(',')
            axios.post(api + 'notes', sendData)
                .then(res => {
                    resolve(new ServerResponse(res.data.result))
                }).catch(err => {
                    reject(new ServerResponse(err.response.data.result))
                })
        })
    }
})
