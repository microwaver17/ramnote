import { Note, Tag } from './models'


export const dummyTags: readonly Tag[] = Object.freeze([
    new Tag(1, 'a'),
    new Tag(2, 'b'),
    new Tag(3, 'c'),
    new Tag(4, 'd'),
    new Tag(5, 'e'),
])

export const dummyNotes: readonly Note[] = Object.freeze([
    new Note(
        1,
        'asdf',
        'fwfgxfgvf',
        new Date(124),
        [dummyTags[0], dummyTags[1]]
    ),
    new Note(
        2,
        'kiuitglor',
        'wery45ujrf',
        new Date(32432452345),
        [dummyTags[0], dummyTags[4]]
    ),
    new Note(
        3,
        'dsgwet45j',
        'syrtqt43w',
        new Date(876345234),
        [dummyTags[2], dummyTags[3]]
    ),
    new Note(
        4,
        'sbdfhjdt',
        'ear54hss',
        new Date(5634523453438),
        [dummyTags[3]]
    ),
])