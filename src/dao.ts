import axios, { AxiosResponse } from 'axios'

import { config } from './config'
import { Note, Tag } from './model'

const api = config.apiRoot

export const dao = Object.freeze({
    getTags(): Promise<Tag[]> {
        return new Promise((resolve, reject) => {
            axios.get(api + 'tags')
                .then(res => {
                    const tags: Tag[] = [];
                    (res.data as []).forEach(tag => {
                        tags.push(new Tag(tag['id'], tag['name']))
                    })
                    resolve(tags)

                }).catch(err => {
                    reject(err.data)
                })
        })
    },

    getNotes(): Promise<Note[]> {
        return new Promise((resolve, reject) => {
            axios.get(api + 'notes')
                .then(res => {
                    const notes: Note[] = [];
                    (res.data as []).forEach(note => {
                        // DB格納形式とJS格納形式の変換
                        const date = new Date(note['date'])
                        const tags = (note['tags'] as string).split(',')
                        notes.push(new Note(note['id'], note['title'], note['body'], date, tags))
                    })
                    resolve(notes)

                }).catch(err => {
                    reject(err.date)
                })

        })
    }
})
