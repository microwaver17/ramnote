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

    clone() {
        return new Note(this.id, this.title, this.body, this.date, this.tags.map(tag => tag.clone()))
    }

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

    clone() {
        return new Tag(this.id, this.name)
    }

    static empty(): Tag {
        return new Tag(null, '')
    }
}

export class ServerResponse {
    constructor(
        public result: string,
    ) { }
}