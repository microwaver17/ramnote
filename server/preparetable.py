import sqlite3
from contextlib import closing
from pathlib import Path
import sys

import config   # noqa


def prepare_table():
    """
    DB・テーブルが存在しなければ作成する
    """

    # DBフォルダの作成
    db_path = config.db_path
    if not db_path.parent.exists():
        db_path.parent.mkdir()

    with closing(sqlite3.connect(config.db_path)) as connection:
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
        else:
            print('スキップ テーブル作成: notes')

        if 'tags' not in tables:
            print('テーブル作成: tags')
            cur.execute("""
                CREATE TABLE tags(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    deleted INTEGER NOT NULL DEFAULT 0
                )
            """)
        else:
            print('スキップ テーブル作成: tags')

        if 'junction_notes_tags' not in tables:
            print('テーブル作成: note_tags')
            cur.execute("""
                CREATE TABLE junction_notes_tags(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL
                )
            """)
        else:
            print('スキップ テーブル作成: note_tags')

        connection.commit()