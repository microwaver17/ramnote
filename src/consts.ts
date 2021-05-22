import { Note, Tag } from './model'

export const dummyNotes: readonly Note[] = Object.freeze([
    new Note(
        0,
        'asdf',
        'fwfgxfgvf',
        new Date(124),
        ['a', 'b',]
    ),
    new Note(
        1,
        'kiuitglor',
        'wery45ujrf',
        new Date(32432452345),
        ['a', 'c',]
    ),
    new Note(
        2,
        'dsgwet45j',
        'syrtqt43w',
        new Date(876345234),
        ['d', 'c',]
    ),
    new Note(
        3,
        'sbdfhjdt',
        'ear54hss',
        new Date(5634523453438),
        ['a', 'c',]
    ),
])

export const dummyTags: readonly Tag[] = Object.freeze([
    new Tag(1, 'a'),
    new Tag(2, 'b'),
    new Tag(3, 'c'),
    new Tag(4, 'd'),
    new Tag(5, 'e'),
])
