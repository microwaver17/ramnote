import sqlite3
from pathlib import Path
import sys
import random
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))
import config   # noqa


def rnd_utc():
    return random.randint(0, int(datetime.today().timestamp()))


testdata_notes = [
    ['ジャンル', 'ロック・ジャズ・ブルース', rnd_utc(), [0]],
    ['使用楽器', 'ギター\n5wayピックアップセレクター\nホワイト', rnd_utc(), [0,1]],
    ['買い物', '卵・ネギ・もやし・ジャンバラヤ・きゅうり', rnd_utc(), [2,5]],
    ['', '宇宙飛行士の弟の背中を追い続ける兄', rnd_utc(), [3,4]],
    ['企画書', 'プレゼン用\nテレワーク推進', rnd_utc(), [2,3]],
    ['確定申告', '〇〇生命のはがきを探す', rnd_utc(), [2,6]],
    ['', 'x + y = z', rnd_utc(), []]
]
testdata_tags = [
    '音楽',
    '作曲',
    'TODO',
    'アイデア',
    '漫画',
    '料理',
    '市役所',
    '未使用'
]

if __name__ == '__main__':
    db_path = config.db_path
    print(f'DBオープン\n{db_path}\n')

    connection = sqlite3.connect(db_path)
    cur = connection.cursor()

    # テーブル存在確認
    tables = [row[1] for row in cur.execute('SELECT * FROM sqlite_master WHERE type="table"')]
    print('テーブル一覧\n' + '\n'.join(tables) + '\n')

    # テーブルがなければ終了
    if 'notes' not in tables \
            or 'tags' not in tables \
            or 'junction_notes_tags' not in tables:
        print('テーブルがありません。')
        quit()

    # データが有れば終了
    notes = list(cur.execute('SELECT * FROM notes'))
    tags = list(cur.execute('SELECT * FROM tags'))
    junction_notes_tags = list(cur.execute('SELECT * FROM junction_notes_tags'))
    if len(notes) != 0 \
            or len(tags) != 0 \
            or len(junction_notes_tags) != 0:
        print('テーブルが空でないので、ダミーデータ―を挿入しません。')
        quit()

    for i, note in enumerate(testdata_notes):
        cur.execute("""
            INSERT INTO notes(id, title, body, date) VALUES(?, ?, ?, ?)
        """, [i] + note[:3])

    for i, tag in enumerate(testdata_tags):
        cur.execute("""
            INSERT INTO tags(id, name) VALUES(?, ?)
        """, (i, tag))

    for i, note in enumerate(testdata_notes):
        for tag_id in note[3]:
            cur.execute("""
                INSERT INTO junction_notes_tags(note_id, tag_id) VALUES (?, ?)
            """, (i, tag_id))

    connection.commit()
    connection.close()