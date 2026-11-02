"""账本存储层：只负责把数据存进文件、从文件读出来"""

import json
import os
import pathlib

EMPTY_LEDGER = {"version": 1, "records": []}


def load_ledger(path):
    
    path = pathlib.Path(path)

    if not path.exists():
        return {"version": 1, "records": []}

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"账本文件损坏：{path}") from e

    if "records" not in data:
        raise ValueError(f"缺少 records 字段：{path}")

    return data


def save_ledger(data, path):
    
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    os.replace(tmp, path)