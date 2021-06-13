import sqlite3
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
import config   # noqa

if __name__ == '__main__':
    db_path = config.db_path
    if not db_path.parent.exists():
        db_path.parent.mkdir()
    print(f'DBオープン\n{db_path}\n')

    connection = sqlite3.connect(db_path)
    cur = connection.cursor()

    # テーブル存在確認
    tables = [row[1] for row in cur.execute('SELECT * FROM sqlite_master WHERE type="table"')]
    print('テーブル一覧\n' + '\n'.join(tables) + '\n')

    # テーブル作成
    if 'notes' not in tables:
        print('テーブル作成: notes')
        cur.execute("""
            CREATE TABLE notes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                date INTEGER NOT NULL,
                deleted INTEGER NOT NULL DEFAULT 0
            )
        """)

    if 'tags' not in tables:
        print('テーブル作成: tags')
        cur.execute("""
            CREATE TABLE tags(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                deleted INTEGER NOT NULL DEFAULT 0
            )
        """)

    if 'junction_notes_tags' not in tables:
        print('テーブル作成: note_tags')
        cur.execute("""
            CREATE TABLE junction_notes_tags(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL
            )
        """)

    connection.commit()
    connection.close()