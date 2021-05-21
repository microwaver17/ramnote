from flask import Flask, request, abort, jsonify, Response
from werkzeug.exceptions import HTTPException
from typing import Union
import sqlite3
from contextlib import closing

import config
import consts

app = Flask(__name__)


def slim(s: str) -> str:
    """文字列を設定した文字数で打ち切る

    Args:
        s: 文字列

    Returns:
        str: 打ち切った文字列

    """
    return s[:config.text_max_length]


def success() -> dict:
    """正常終了時のレスポンスを生成

    Returns:
        dict: レスポンス

    """
    return {'result': consts.SUCCESS}


@app.errorhandler(HTTPException)
def server_error(e: HTTPException) -> tuple[dict, int]:
    """サーバーエラーをJSONで返すハンドラ

    Args:
        e (HTTPException): 例外

    Returns:
        tuple: レスポンス, ステータスコード

    """
    cause = e.description if e.description is not None else consts.ErrorCauses.UNKNOWN
    return {'cause': cause}, e.code


@app.route('/api/notes', methods=['GET', 'POST'])
def notes_list_or_register() -> Union[dict, Response]:
    """ノートの取得・登録

    URL
        /api/notes
    POST
        * title (str)
        * body (str)
        * date (int)
        * tags (str)

    Returns:
        Union[dict, Response]: レスポンス

    """
    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            cur = connection.cursor()

            # 取得
            if request.method == 'GET':
                notes = cur.execute("""
                    SELECT * FROM notes
                """)
                res = [dict(zip(('id', 'title', 'body', 'date', 'tags'), note)) for note in notes]

                return jsonify(res)

            # 登録
            else:
                if not request.is_json:
                    abort(400, description=consts.ErrorCauses.IS_NOT_JSON)
                json: dict = request.json

                # タグが tags テーブルに存在するか確認
                tags = json['tags'].split(',')
                for tag in tags:
                    ret = cur.execute("""
                        SELECT count(*) FROM tags WHERE tag=?
                    """, (tag, ))
                    if ret.fetchone()[0] == 0:
                        # タグがなければ登録しない
                        abort(400, description=consts.ErrorCauses.TAG_NOT_FOUND)

                # 追加
                cur.execute("""
                    INSERT INTO notes(title, body, date, tags) VALUES(?, ?, ?, ?)
                """, (slim(json['title']), slim(json['body']), json['date'], slim(json['tags'])))

                connection.commit()
                return success()

    except sqlite3.Error:
        abort(500, description=consts.ErrorCauses.DB)


@app.route('/api/notes/<pk>', methods=['POST'])
def notes_update(pk) -> dict:
    """ノートの更新

    URL
        /api/notes/<id>
    POST
        * title (str)
        * body (str)
        * date (int)
        * tags (str)

    Args:
        pk (str): 更新するノートのID

    Returns:
        dict:   レスポンス

    """
    if not request.is_json:
        abort(400, description=consts.ErrorCauses.IS_NOT_JSON)

    pk = int(pk)
    json: dict = request.json

    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            cur = connection.cursor()

            # タグが tags テーブルに存在するか確認
            tags = json['tags'].split(',')
            for tag in tags:
                ret = cur.execute("""
                    SELECT count(*) FROM tags WHERE tag=?
                """, (tag,))
                if ret.fetchone()[0] == 0:
                    # タグがなければ登録しない
                    abort(400, description=consts.ErrorCauses.TAG_NOT_FOUND)

            cur.execute("""
                UPDATE notes SET 
                title=?, body=?, date=?, tags=?
                WHERE id=?
            """, (json['title'], json['body'], json['date'], json['tags'], pk))
            if cur.rowcount == 0:
                abort(400, description=consts.ErrorCauses.NOTE_NOT_FOUND)
            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ErrorCauses.DB)

    return success()


@app.route('/api/notes/<pk>/delete', methods=['POST'])
def notes_delete(pk) -> dict:
    """ノートの削除

    URL
        /api/notes/<id>/delete
    POST
        なんでもいい

    Args:
        pk (str): 削除するノートのID

    Returns:
        dict: レスポンス

    """
    pk = int(pk)
    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            cur = connection.cursor()
            cur.execute("""
                DELETE FROM notes where id=?
            """, (pk, ))
            if cur.rowcount == 0:
                abort(400, description=consts.ErrorCauses.NOTE_NOT_FOUND)
            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ErrorCauses.DB)

    return success()


@app.route('/api/tags', methods=['GET', 'POST'])
def tags_list_or_register() -> Union[dict, Response]:
    """タグの取得・登録

    URL
        /api/tags
    POST
        name (str)

    Returns:
        Union[dict, Response]: レスポンス

    """
    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            cur = connection.cursor()

            # 取得
            if request.method == 'GET':
                tags = cur.execute("""
                    SELECT * FROM tags
                """)
                res = [dict(zip(('id', 'name'), tag)) for tag in tags]

                return jsonify(res)

            # 登録
            else:
                if not request.is_json:
                    abort(400, description=consts.ErrorCauses.IS_NOT_JSON)
                json: dict = request.json

                # 重複タグが存在するか確認
                res = cur.execute("""
                    SELECT COUNT(*) FROM tags WHERE name=?
                """, (json['name'], ))
                if res.fetchone()[0] != 0:
                    abort(400, description=consts.ErrorCauses.TAG_DUPLICATED)

                # 追加
                cur.execute("""
                    INSERT INTO tags(name) VALUES(?)
                """, (slim(json['name']), ))

                connection.commit()
                return success()

    except sqlite3.Error:
        abort(500, description=consts.ErrorCauses.DB)


@app.route('/api/tags/<pk>/delete', methods=['POST'])
def tags_delete(pk: str) -> dict:
    """タグの削除

    URL
        /api/tags/<id>/delete
    POST
        なんでもいい

    Args:
        pk:

    Returns:
        dict: レスポンス

    """
    pk = int(pk)
    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            cur = connection.cursor()
            cur.execute("""
                DELETE FROM tags where id=?
            """, (pk, ))
            if cur.rowcount == 0:
                abort(400, description=consts.ErrorCauses.TAG_NOT_FOUND)
            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ErrorCauses.DB)

    return success()