import { Carousel } from "bootstrap"

// ノートの定義
export class Note {
    constructor(
        public id: number | null,   //nullなら新規作成
        public title: string,
        public body: string,
        public date: Date,
        public tags: Tag[],
    ) { }

    static empty(): Note {
        return new Note(null, '', '', new Date(), [])
    }
}

// タグの定義
export class Tag {
    constructor(
        public id: number | null,   //nullなら新規作成
        public name: string
    ) { }

    static empty(): Tag {
        return new Tag(null, '')
    }
}

export class ServerResponse {
    constructor(
        public result: string,
    ) { }
}