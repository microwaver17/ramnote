import sqlite3
from pathlib import Path
import sys
import random

sys.path.append(str(Path(__file__).parent.parent))
import config   # noqa


def rnd_utc():
    return random.randint(1, 1621523080993)


testdata_notes = [
    ['ジャンル', 'ロック', rnd_utc(), '1'],
    ['使用楽器', 'ギター', rnd_utc(), '1,2'],
    ['買い物', '卵,ネギ,もやし', rnd_utc(), '3'],
    ['', 'SF', rnd_utc(), '4,5'],
    ['企画書', '', rnd_utc(), '3,4'],
]
testdata_tags = [
    '音楽',
    '作曲',
    'TODO',
    'アイデア',
    '漫画',
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
    if 'notes' not in tables or 'tags' not in tables:
        print('テーブルがありません。')
        quit()

    # データが有れば終了
    notes = list(cur.execute('SELECT * FROM notes'))
    tags = list(cur.execute('SELECT * FROM tags'))
    if len(notes) != 0 or len(tags) != 0:
        print('テーブルが空でないので、ダミーデータ―を挿入しません。')
        quit()

    for note in testdata_notes:
        cur.execute("""
            INSERT INTO notes(title, body, date, tag_ids) VALUES(?, ?, ?, ?)
        """, note)

    for tag in testdata_tags:
        cur.execute("""
            INSERT INTO tags(name) VALUES(?)
        """, (tag, ))

    connection.commit()
    connection.close()