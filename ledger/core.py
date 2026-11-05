"""账本业务层：纯逻辑，不碰文件、不打印"""

import datetime
from decimal import Decimal, InvalidOperation

KINDS = ("expense", "income")

KIND_LABELS = {
    "expense": "支出",
    "income": "收入",
}


def parse_amount(text):
    """金额字符串 → 整数分（正数）。非法输入抛 ValueError。"""
    try:
        value = Decimal(str(text).strip())
    except InvalidOperation:
        raise ValueError(f"金额格式不对：{text!r}") from None

    cents = value * 100
    if cents != cents.to_integral_value():
        raise ValueError(f"金额最多两位小数：{text!r}")

    result = int(cents)
    if result <= 0:
        raise ValueError(f"金额必须大于 0：{text!r}")

    return result


def next_id(data, date_str):
    """生成 20261102-001 形式的 ID。"""
    day = date_str.replace("-", "")
    prefix = f"{day}-"

    max_seq = 0
    for record in data["records"]:
        rid = record.get("id", "")
        if not rid.startswith(prefix):
            continue
        tail = rid[len(prefix):]
        if tail.isdigit():
            max_seq = max(max_seq, int(tail))

    return f"{prefix}{max_seq + 1:03d}"


def add_record(
    data,
    amount_text,
    note,
    date_str=None,
    category="未分类",
    kind="expense",
):
    """新增一笔，返回新记录的 dict。不负责存盘。

    金额永远按正数输入，符号由 kind 决定：
        expense -> amount_cents 为负
        income  -> amount_cents 为正
    """
    if date_str is None:
        date_str = datetime.date.today().isoformat()

    if kind not in KIND_LABELS:
        raise ValueError(f"类型不对：{kind!r}")

    cents = parse_amount(amount_text)

    record = {
        "id": next_id(data, date_str),
        "date": date_str,
        "kind": kind,
        "amount_cents": -cents if kind == "expense" else cents,
        "note": note,
        "category": category,
    }
    data["records"].append(record)
    return record


def list_records(data, month=None, limit=10, category=None):
    """按日期倒序返回记录列表。month 形如 2026-11。"""
    records = data["records"]
    if month:
        records = [r for r in records if r["date"].startswith(month)]
    if category:
        records = [r for r in records if r["category"] == category]
    records = sorted(records, key=lambda r: (r["date"], r["id"]), reverse=True)
    if limit is not None:
        records = records[:limit]
    return records


def summarize(data, month=None):
    """返回 {"count", "expense_cents", "income_cents", "balance_cents", "by_category"}。

    expense_cents / income_cents 都是正数；by_category 只统计支出。
    """
    records = list_records(data, month=month, limit=None)

    expense = 0
    income = 0
    by_category = {}

    for r in records:
        cents = r["amount_cents"]
        if cents < 0:
            expense += -cents
            cat = r["category"]
            by_category[cat] = by_category.get(cat, 0) + (-cents)
        else:
            income += cents

    return {
        "count": len(records),
        "expense_cents": expense,
        "income_cents": income,
        "balance_cents": income - expense,
        "by_category": by_category,
    }

def update_record(
    data,
    record_id,
    amount_text=None,
    note=None,
    date_str=None,
    category=None,
    kind=None,
):
    """改一笔记录。只改传入的字段，None 表示不动。找不到抛 ValueError。"""
    record = None
    for r in data["records"]:
        if r["id"] == record_id:
            record = r
            break

    if record is None:
        raise ValueError(f"找不到这笔记录：{record_id}")

    if kind is not None:
        if kind not in KIND_LABELS:
            raise ValueError(f"类型不对：{kind!r}")
        record["kind"] = kind
        cents = abs(record["amount_cents"])
        record["amount_cents"] = -cents if kind == "expense" else cents

    if amount_text is not None:
        cents = parse_amount(amount_text)
        record["amount_cents"] = -cents if record["kind"] == "expense" else cents

    if note is not None:
        record["note"] = note

    if category is not None:
        record["category"] = category

    if date_str is not None:
        record["date"] = date_str

    return record

def delete_record(data, record_id):
    """删除指定记录并返回它；找不到抛 ValueError。"""
    for index, record in enumerate(data["records"]):
        if record["id"] == record_id:
            return data["records"].pop(index)
    raise ValueError(f"找不到这笔记录：{record_id}")



def format_cents(cents):
    """整数分 → 显示用的元，带符号：-3500 → '-35.00'。"""
    return f"{cents / 100:.2f}"


EXPORT_HEADER = ["单号", "日期", "类型", "金额(元)", "分类", "说明"]


def to_export_rows(data, month=None):
    """导出用的二维表：第一行是表头，金额带符号、单位元。"""
    rows = [list(EXPORT_HEADER)]
    for record in list_records(data, month=month, limit=None):
        rows.append(
            [
                record["id"],
                record["date"],
                KIND_LABELS[record["kind"]],
                format_cents(record["amount_cents"]),
                record["category"],
                record["note"],
            ]
        )
    return rows