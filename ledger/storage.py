"""账本存储层：只负责把数据存进文件、从文件读出来"""

import json
import os
import pathlib

CURRENT_VERSION = 2
EMPTY_LEDGER = {"version": CURRENT_VERSION, "records": []}

KIND_VALUES = ("expense", "income")


def migrate(data):
    """把数据升级 / 修补到当前版本。就地修改并返回。

    做三件事：
    1. 每条记录都要有 kind；缺了或值不对，按规则推断（见下）
    2. 金额符号与 kind 对齐（支出为负、收入为正）
    3. 版本号低于当前版本时升级

    这个函数是幂等的：合法数据跑一遍不会变。
    """
    version = data.get("version", 1)

    for record in data.get("records", []):
        cents = record.get("amount_cents", 0)
        kind = record.get("kind")

        if kind not in KIND_VALUES:
            if version < 2:
                # v1 的约定：金额一律是正数，而且全是支出
                kind = "expense"
            else:
                # v2 缺 kind 说明数据坏了，只能按金额符号猜
                kind = "expense" if cents <= 0 else "income"
            record["kind"] = kind

        record["amount_cents"] = -abs(cents) if kind == "expense" else abs(cents)

    if version < CURRENT_VERSION:
        data["version"] = CURRENT_VERSION

    return data


def load_ledger(path):
    """读账本。文件不存在返回空账本；内容损坏抛 ValueError。"""
    path = pathlib.Path(path)

    if not path.exists():
        return {"version": CURRENT_VERSION, "records": []}

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"账本文件损坏：{path}") from e

    if "records" not in data:
        raise ValueError(f"账本文件格式不对：缺少 records 字段（{path}）")

    return migrate(data)


def save_ledger(data, path):
    """存账本。自动建目录；原子写入。"""
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    os.replace(tmp, path)