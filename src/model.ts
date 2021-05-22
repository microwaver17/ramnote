// ノートの定義
export class Note {
    constructor(
        public id: number | null,
        public title: string,
        public body: string,
        public date: Date,
        public tags_str: string[],
    ) { }

    static empty(): Note {
        return new Note(null, '', '', new Date(), [])
    }
}

// タグの定義
export class Tag {
    constructor(
        public id: number | null,
        public name: string
    ) { }

    static empty(): Tag {
        return new Tag(null, '')
    }
}