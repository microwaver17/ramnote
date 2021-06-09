import { Note, Tag } from './models'

export class consts {
    static dummyTags = Object.freeze([
        new Tag(1, 'a'),
        new Tag(2, 'b'),
        new Tag(3, 'c'),
        new Tag(4, 'd'),
        new Tag(5, 'e'),
    ])

    static dummyNotes = Object.freeze([
        new Note(
            1,
            'asdf',
            'fwfgxfgvf',
            new Date(124),
            [consts.dummyTags[0], consts.dummyTags[1]]
        ),
        new Note(
            2,
            'kiuitglor',
            'wery45ujrf',
            new Date(32432452345),
            [consts.dummyTags[0], consts.dummyTags[4]]
        ),
        new Note(
            3,
            'dsgwet45j',
            'syrtqt43w',
            new Date(876345234),
            [consts.dummyTags[2], consts.dummyTags[3]]
        ),
        new Note(
            4,
            'sbdfhjdt',
            'ear54hss',
            new Date(5634523453438),
            [consts.dummyTags[3]]
        ),
    ])

    private constructor() { return false }
}
