import axios, { AxiosResponse } from 'axios'

import { config } from './config'
import { Note, Tag, ServerResponse } from './models'

const api = config.apiRoot

// サーバーエラーと then 内のエラーの両方に対応する
function getErrorResponse(err: any) {
    if (err.response) {
        if (err.response.data.result) {
            return new ServerResponse(err.response.data.result)
        } else {
            return new ServerResponse('サーバーエラー')
        }
    }
    console.error(err)
    return new ServerResponse('クライアントエラー')
}

export const dao = Object.freeze({
    getTags(): Promise<Tag[]> {
        return new Promise((resolve, reject) => {
            axios.get(api + 'tags')
                .then(res => {
                    const tags = (res.data as Array<any>).map(tag => new Tag(tag['id'], tag['name'], tag['used_count']))
                    resolve(tags)

                }).catch(err => {
                    reject(getErrorResponse(err))
                })
        })
    },

    getNotes(keyword = '', tags: Tag[] = [], date_from = -1, date_to = -1): Promise<Note[]> {
        return new Promise((resolve, reject) => {
            const params: any = {}
            if (keyword) { params.keyword = keyword }
            if (tags.length > 0) { params['tag-ids'] = tags.map(tag => tag.id).join(',') }
            if (date_from >= 0) { params['date-from'] = date_from }
            if (date_to >= 0) { params['date-to'] = date_to }
            axios.get(api + 'notes', { params: params })
                .then(res => {
                    const notes = (res.data as Array<any>).map(note => {
                        const tags = (note.tags as Array<any>).map(tag => new Tag(tag.id, tag.name, -1))
                        const date = new Date(note.date)    // DB側ではUNIX時間で格納しているので変換する
                        return new Note(note.id, note.title, note.body, date, tags)
                    })
                    resolve(notes)

                }).catch(err => {
                    reject(getErrorResponse(err))
                })
        })
    },

    createNote(note: Note): Promise<ServerResponse> {
        return new Promise((resolve, reject) => {
            const sendData: any = Object.assign({}, note)
            sendData.date = sendData.date.getTime()     // DB側ではUNIX時間で格納しているので変換する
            axios.post(api + 'notes', sendData)
                .then(res => {
                    resolve(new ServerResponse(res.data.result))
                }).catch(err => {
                    reject(getErrorResponse(err))
                })
        })
    },

    updateNote(note: Note): Promise<ServerResponse> {
        return new Promise((resolve, reject) => {
            const sendData: any = Object.assign({}, note)
            sendData.date = sendData.date.getTime()     // DB側ではUNIX時間で格納しているので変換する
            axios.post(api + 'notes/' + sendData.id, sendData)
                .then(res => {
                    resolve(new ServerResponse(res.data.result))
                }).catch(err => {
                    reject(getErrorResponse(err))
                })
        })
    },

    deleteNote(note: Note): Promise<ServerResponse> {
        return new Promise((resolve, reject) => {
            axios.post(api + 'notes/' + note.id + '/delete')
                .then(res => {
                    resolve(new ServerResponse(res.data.result))
                }).catch(err => {
                    reject(getErrorResponse(err))
                })
        })
    },

    createTag(tag: Tag): Promise<ServerResponse> {
        return new Promise((resolve, reject) => {
            axios.post(api + 'tags', tag)
                .then(res => {
                    resolve(new ServerResponse(res.data.result))
                }).catch(err => {
                    reject(getErrorResponse(err))
                })
        })
    },
})
