import sqlite3
from pathlib import Path
import sys
import random

sys.path.append(str(Path(__file__).parent.parent))
import config   # noqa


def rnd_utc():
    return random.randint(1, 1621523080993)


testdata_notes = [
    ['ビートルズ', 'ヒア・カムズ・ザ・サン', rnd_utc(), '音楽'],
    ['使用楽器', 'ストラトキャスタ―', rnd_utc(), '音楽,作曲'],
    ['買い物', '卵,ネギ,もやし', rnd_utc(), 'TODO'],
    ['物語案', '老人に生まれて若くなっていった先のきらら系', rnd_utc(), 'アイデア,漫画'],
    ['', '上野さんは2巻まで持ってる', rnd_utc(), '漫画,TODO'],
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
            INSERT INTO notes(title, body, date, tags) VALUES(?, ?, ?, ?)
        """, note)

    for tag in testdata_tags:
        cur.execute("""
            INSERT INTO tags(name) VALUES(?)
        """, (tag, ))

    connection.commit()
    connection.close()