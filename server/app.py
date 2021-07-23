import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent)) # embedded python で起動するためpy

import datetime
from flask import Flask, request, abort, jsonify, Response, make_response
from werkzeug.exceptions import HTTPException
from typing import Union, Optional
import sqlite3
from contextlib import closing
from datetime import datetime


import config
import consts
from preparetable import prepare_table

app = Flask(__name__)


def slim(s: str) -> str:
    """文字列を設定した文字数で打ち切る"""
    return s[:config.text_max_length]


def extract_tags(tags_str: str) -> list[int]:
    """コンマ区切り文字列をタグIDのリストに分割"""
    if tags_str == '':
        return []

    tags = tags_str.split(',')
    return sorted([int(tag) for tag in tags])


def concat_tag_ids(tag_ids: list[int]) -> str:
    """タグIDのリストをコンマ区切り文字列に結合"""
    tag_ids = sorted(tag_ids)
    return ','.join([str(tag_id) for tag_id in tag_ids])


def jstime_to_dbtime(jstime: int):
    """Javascriptの時刻からDBの時刻へ変換"""
    return jstime // 1000


def dbtime_to_jstime(dbtime: int):
    """DBの時刻からJavascriptの時刻へ変換"""
    return dbtime * 1000


def response(result: str) -> dict:
    """HTTPレスポンスを生成"""
    return {'result': result}


@app.errorhandler(HTTPException)
def server_error(e: HTTPException) -> tuple[dict, int]:
    """サーバーエラーをJSONで返すハンドラ

    Args:
        e (HTTPException): 例外

    Returns:
        tuple: レスポンス, ステータスコード

    """
    cause = e.description if e.description is not None else consts.ResultMessage.UNKNOWN
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
        * tags (dict)
            * id (int)
            * name (int)

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
                date_from = request.args.get('date-from', -1)
                date_to = request.args.get('date-to', -1)
                tag_ids = extract_tags(tag_ids_str)

                print(request.full_path)
                params = [0, f'%{keyword}%', f'%{keyword}%', f'%{keyword}%']
                sql = """
                    SELECT GROUP_CONCAT(tags.id) as tag_ids_str, * FROM notes
                        LEFT OUTER JOIN junction_notes_tags
                            on notes.id = junction_notes_tags.note_id
                        LEFT OUTER JOIN tags
                            on tags.id = junction_notes_tags.tag_id
                        WHERE notes.deleted=?
                            AND (notes.title LIKE ? OR notes.body LIKE ? OR tags.name LIKE ?) 
                """
                if date_from != -1:
                    sql += 'AND notes.date > ?\n'
                    params.append(jstime_to_dbtime(date_from))
                if date_to != -1:
                    sql += 'AND notes.date < ?\n'
                    params.append(jstime_to_dbtime(date_to))
                if len(tag_ids) > 0:
                    sql += 'AND tags.id IN(' + ','.join(['?' for i in range(len(tag_ids))]) + ')\n'
                    params += tag_ids
                sql += """
                        GROUP BY notes.id
                        ORDER BY notes.date DESC
                """
                print(sql)
                print(params)
                notes = cur.execute(sql, params).fetchall()

                res = []
                for note in notes:
                    if len(tag_ids) > 0 and extract_tags(note['tag_ids_str']) != tag_ids:
                        continue
                    rows = cur.execute("""
                        SELECT tags.id as id, tags.name as name FROM junction_notes_tags
                            INNER JOIN tags
                                ON tags.id = junction_notes_tags.tag_id
                        WHERE junction_notes_tags.note_id=?
                    """, (note['id'], )).fetchall()
                    tags = [{'id': row['id'], 'name': row['name']} for row in rows]

                    res.append({
                        'id': note['id'],
                        'title': note['title'],
                        'body': note['body'],
                        'date': dbtime_to_jstime(note['date']),
                        'tags': tags
                    })
                return jsonify(res)

            # 登録
            else:
                if not request.is_json:
                    abort(400, description=consts.ResultMessage.IS_NOT_JSON)
                json: dict = request.json

                # タグが存在するか確認
                
                for tag in json['tags']:
                    rows = cur.execute("""
                        SELECT count(*) FROM tags WHERE id=? AND deleted=?
                    """, (tag['id'], 0))
                    if rows.fetchone()[0] == 0:
                        abort(400, description=consts.ResultMessage.TAG_NOT_FOUND)

                # 追加
                res = cur.execute("""
                    INSERT INTO notes(title, body, date) VALUES(?, ?, ?)
                """, (slim(json['title']), slim(json['body']), jstime_to_dbtime(json['date']), ))
                note_id = res.lastrowid

                for tag in json['tags']:
                    cur.execute("""
                        INSERT INTO junction_notes_tags(note_id, tag_id) VALUES (?, ?)
                    """, (note_id, tag['id']))

                connection.commit()
                return response(consts.ResultMessage.SUCCESS)

    except sqlite3.Error as e:
        abort(500, description=(consts.ResultMessage.DB + ' ' + str(e)))


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
        abort(400, description=consts.ResultMessage.IS_NOT_JSON)

    pk = int(pk)
    json: dict = request.json

    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()

            # タグが存在するか確認
            for tag in json['tags']:
                rows = cur.execute("""
                    SELECT count(*) FROM tags WHERE id=? AND deleted=?
                """, (tag['id'], 0))
                if rows.fetchone()[0] == 0:
                    abort(400, description=consts.ResultMessage.TAG_NOT_FOUND)

            cur.execute("""
                UPDATE notes SET 
                title=?, body=?, date=?
                WHERE id=?
            """, (slim(json['title']), slim(json['body']), jstime_to_dbtime(json['date']), pk))
            if cur.rowcount == 0:
                abort(400, description=consts.ResultMessage.NOTE_NOT_FOUND)

            cur.execute("""
                DELETE FROM junction_notes_tags WHERE note_id=?
            """, (pk, ))

            for tag in json['tags']:
                cur.execute("""
                    INSERT INTO junction_notes_tags(note_id, tag_id) VALUES (?, ?)
                """, (pk, tag['id']))

            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ResultMessage.DB)

    return response(consts.ResultMessage.SUCCESS)


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
                abort(400, description=consts.ResultMessage.NOTE_NOT_FOUND)
            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ResultMessage.DB)

    return response(consts.ResultMessage.SUCCESS)


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
                    SELECT tags.id, 
                            tags.name, 
                            count(notes.id) as used_count 
                        FROM tags 
                        LEFT OUTER JOIN junction_notes_tags
                            ON tags.id = junction_notes_tags.tag_id
                        LEFT OUTER JOIN notes
                            ON notes.id = junction_notes_tags.note_id 
                            AND notes.deleted=?
                        WHERE tags.deleted=?
                        GROUP BY tags.id
                        ORDER BY used_count DESC
                """, (0, 0))
                res = [dict(zip(('id', 'name', 'used_count'), tag)) for tag in tags]

                return jsonify(res)

            # 登録
            else:
                if not request.is_json:
                    abort(400, description=consts.ResultMessage.IS_NOT_JSON)
                json: dict = request.json

                # 重複タグが存在するか確認
                rows = cur.execute("""
                    SELECT count(*) FROM tags WHERE name=? AND deleted=?
                """, (json['name'], 0))
                if rows.fetchone()[0] == 1:
                    abort(400, description=consts.ResultMessage.TAG_DUPLICATED)

                # 追加
                cur.execute("""
                    INSERT INTO tags(name) VALUES(?)
                """, (slim(json['name']), ))

                connection.commit()
                return response(consts.ResultMessage.SUCCESS)

    except sqlite3.Error as e:
        print(e)
        abort(500, description=consts.ResultMessage.DB)


@app.route('/api/tags/<pk>/delete', methods=['POST'])
def tags_delete(pk: str) -> dict:
    """タグの削除

    URL
        /api/tags/<id>/delete
    POST
        なんでもいい

    Args:
        pk: 削除するタグのID

    Returns:
        dict: レスポンス

    """
    pk = int(pk)
    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()
            cur.execute("""
                UPDATE tags SET deleted=? WHERE id=?
            """, (1, pk))
            if cur.rowcount == 0:
                abort(400, description=consts.ResultMessage.TAG_NOT_FOUND)
            connection.commit()
    except sqlite3.Error:
        abort(500, description=consts.ResultMessage.DB)

    return response(consts.ResultMessage.SUCCESS)


def csv_escape(text: str) -> str:
    """CSVのセルをエスケープ"""
    return '"' + str(text).replace('"', '""') + '"'


@app.route('/api/export/csv')
def export_csv():
    """CSV形式（Shift-JIS）でエクスポート

    URL
        /api/export/csv

    Returns:
        Response: レスポンス

    """
    try:
        with closing(sqlite3.connect(config.db_path)) as connection:
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()

            keyword = request.args.get('keyword', '')
            tag_ids_str = request.args.get('tag-ids', '')
            date_from = request.args.get('date-from', -1)
            date_to = request.args.get('date-to', -1)
            tag_ids = extract_tags(tag_ids_str)

            print(request.full_path)
            params = [0, f'%{keyword}%', f'%{keyword}%', f'%{keyword}%']

            sql = """
                SELECT 
                        notes.title as title, 
                        notes.body as body, 
                        GROUP_CONCAT(tags.name, ',') as tags,
                        notes.date as date 
                    FROM notes
                    LEFT OUTER JOIN junction_notes_tags
                        on notes.id = junction_notes_tags.note_id
                    LEFT OUTER JOIN tags
                        on tags.id = junction_notes_tags.tag_id
                    WHERE notes.deleted=?
                        AND (notes.title LIKE ? OR notes.body LIKE ? OR tags.name LIKE ?) 
            """
            if date_from != -1:
                sql += 'AND notes.date > ?\n'
                params.append(jstime_to_dbtime(date_from))
            if date_to != -1:
                sql += 'AND notes.date < ?\n'
                params.append(jstime_to_dbtime(date_to))
            if len(tag_ids) > 0:
                sql += 'AND tags.id IN(' + ','.join(['?' for i in range(len(tag_ids))]) + ')\n'
                params += tag_ids
            sql += """
                    GROUP BY notes.id
                    ORDER BY notes.date DESC
            """
            print(sql)
            print(params)

            notes = cur.execute(sql, params).fetchall()

            lines: list[str] = [','.join([csv_escape(head) for head in ['タイトル', '本文', 'タグ', '日付']])]
            for note in notes:
                line = []
                line.append(note['title'])
                line.append(note['body'])
                line.append(note['tags'])
                print(note['date'])
                line.append(datetime.fromtimestamp(note['date']).strftime('%Y/%m/%d'))
                line_str = ','.join([csv_escape(str(val)) for val in line])
                lines.append(line_str)

            now_str = datetime.today().strftime('%Y%m%d_%H%M%S')
            res = make_response()
            res.data = '\r\n'.join(lines).encode('sjis', 'backslashreplace')
            #res.headers['Content-Type'] = 'text/plain; charset=Shift-JIS'
            res.headers['Content-Type'] = 'text/csv; charset=Shift-JIS'
            res.headers['Content-Disposition'] = f'attachment; filename=ramnote_{now_str}.csv'

            return res

    except sqlite3.Error:
        abort(500, description=consts.ResultMessage.DB)

if __name__ == '__main__':
    prepare_table()
    app.run('127.0.0.1', consts.PORT, debug=False)