from pathlib import Path

db_path = Path(__file__).parent / 'data' / 'ramnote.db'
"""DBのパス"""

text_max_length = 1024
"""DBに格納する最大文字数"""