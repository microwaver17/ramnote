from flask import Flask, request, abort, jsonify, Response
from werkzeug.exceptions import HTTPException
from typing import Union, Optional
import sqlite3
from contextlib import closing

import config
import consts

app = Flask(__name__)


def slim(s: str) -> str:
    """文字列を設定した文字数で打ち切る"""
    return s[:config.text_max_length]


def extract_tags(tags_str: str) -> list[str]:
    """コンマ区切り文字列をタグIDのリストに分割"""
    if tags_str == '':
        return []

    tags = tags_str.split(',')
    tags = sorted(tags)
    return tags


def concat_tag_ids(tag_ids: list[int]) -> str:
    """タグIDのリストをコンマ区切り文字列に結合"""
    tag_ids = sorted(tag_ids)
    return ','.join([str(tag_id) for tag_id in tag_ids])


def response(result: str) -> dict:
    """HTTPレスポンスを生成"""
    return {'result': result}


def is_tag_exist(tag_id: int, cur: sqlite3.Cursor) -> bool:
    """タグが tags テーブルに存在するか確認"""
    ret = cur.execute("""
        SELECT count(*) FROM tags WHERE id=?
    """, (tag_id,))
    if ret.fetchone()[0] == 1:
        return True
    return False


@app.errorhandler(HTTPException)
def server_error(e: HTTPException) -> tuple[dict, int]:
    """サーバーエラーをJSONで返すハンドラ

    Args:
        e (HTTPException): 例外

    Returns:
        tuple: レスポンス, ステータスコード

    """
    cause = e.description if e.description is not None else consts.ErrorCauses.UNKNOWN
    return response(cause), e.code


@app.route('/api/notes', methods=['GET', 'POST'])
def notes_list_or_register() -> Union[dict, Response]:
    """ノートの取得・登録

    URL
        /api/notes
    GET
        * keyword (str)
        * tag-ids (str) idのコンマ区切り
        * date-from (int)
        * date-to (int)
    POST
        * title (str)
        * body (str)
        * date (int)
        * tag_ids (int)

    Returns:
        Union[dict, Response]: レスポンス

    """
    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()

            # 取得
            if request.method == 'GET':
                keyword = request.args.get('keyword', '')
                tag_ids_str = request.args.get('tag-ids', '')
                date_from = request.args.get('date-from', 0)
                date_to = request.args.get('date-to', 2**64 // 2 - 1)

                tag_ids = extract_tags(tag_ids_str)
                tag_ids_like = '%' + '%'.join([str(tag_id) for tag_id in tag_ids]) + '%'

                print(request.full_path)

                notes = cur.execute("""
                    SELECT * FROM notes 
                        WHERE deleted=? 
                        AND (title LIKE ? OR body LIKE ?) 
                        AND tag_ids LIKE ? 
                        AND date > ?
                        AND date < ?
                        ORDER BY date
                """, (0, f'%{keyword}%', f'%{keyword}%', tag_ids_like, date_from, date_to)).fetchall()

                res = []
                for note in notes:
                    # コンマ区切りのIDで記録されている tag の name を取得
                    tags = []
                    tag_ids = extract_tags(note['tag_ids'])
                    for tag_id in tag_ids:
                        tag_name = cur.execute("""
                            SELECT * FROM tags WHERE id=?
                        """, (tag_id, )).fetchone()['name']
                        tags.append({'id': tag_id, 'name': tag_name})

                    res.append({
                        'id': note['id'],
                        'title': note['title'],
                        'body': note['body'],
                        'date': note['date'],
                        'tags': tags
                    })
                return jsonify(res)

            # 登録
            else:
                if not request.is_json:
                    abort(400, description=consts.ErrorCauses.IS_NOT_JSON)
                json: dict = request.json

                # タグが存在するか確認
                for tag in json['tags']:
                    if not is_tag_exist(tag['id'], cur):
                        abort(400, description=consts.ErrorCauses.TAG_NOT_FOUND)

                tag_ids = concat_tag_ids([tag['id'] for tag in json['tags']])

                # 追加
                cur.execute("""
                    INSERT INTO notes(title, body, date, tag_ids) VALUES(?, ?, ?, ?)
                """, (slim(json['title']), slim(json['body']), json['date'], slim(tag_ids)))

                connection.commit()
                return response(consts.SUCCESS)

    except sqlite3.Error as e:
        abort(500, description=(consts.ErrorCauses.DB + ' ' + str(e)))


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
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()

            # タグが存在するか確認
            for tag in json['tags']:
                if not is_tag_exist(tag['id'], cur):
                    abort(400, description=consts.ErrorCauses.TAG_NOT_FOUND)

            tag_ids = concat_tag_ids([tag['id'] for tag in json['tags']])

            cur.execute("""
                UPDATE notes SET 
                title=?, body=?, date=?, tag_ids=?
                WHERE id=?
            """, (slim(json['title']), slim(json['body']), json['date'], slim(tag_ids), pk))
            if cur.rowcount == 0:
                abort(400, description=consts.ErrorCauses.NOTE_NOT_FOUND)
            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ErrorCauses.DB)

    return response(consts.SUCCESS)


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
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()
            cur.execute("""
                UPDATE notes SET deleted=? WHERE id=?
            """, (1, pk))
            if cur.rowcount == 0:
                abort(400, description=consts.ErrorCauses.NOTE_NOT_FOUND)
            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ErrorCauses.DB)

    return response(consts.SUCCESS)


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
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()

            # 取得
            if request.method == 'GET':
                tags = cur.execute("""
                    SELECT * FROM tags WHERE deleted=0
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
                return response(consts.SUCCESS)

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
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()
            cur.execute("""
                UPDATE tags SET deleted=? WHRER id=?
            """, (1, pk))
            if cur.rowcount == 0:
                abort(400, description=consts.ErrorCauses.TAG_NOT_FOUND)
            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ErrorCauses.DB)

    return response(consts.SUCCESS)
