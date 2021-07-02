PORT = 51803

class ResultMessage:
    """エラー原因を表す文字列定義"""

    UNKNOWN = 'unknown'
    """不明なエラー"""

    DB = 'db'
    """データベースのエラー"""

    NOTE_NOT_FOUND = 'note_not_found'
    """ノートが存在しない"""

    TAG_NOT_FOUND = 'tag_not_found'
    """タグが存在しない"""

    TAG_DUPLICATED = 'tag_duplicated'
    """"重複するタグが追加されようとした"""

    IS_NOT_JSON = 'is_not_json'
    """POSTの形式がJSONでなかった"""

    SUCCESS = 'ok'
    """成功"""
