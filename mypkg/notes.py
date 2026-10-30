"""笔记的 json 存取（从 week6.py 搬出来的）"""

import json


def save_notes(notes, path):
    """把字典存成 JSON 文件"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def load_notes(path):
    """读 JSON 文件；文件不存在时返回 {}"""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}