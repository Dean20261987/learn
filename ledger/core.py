"""账本业务层：纯逻辑，不碰文件、不打印"""

import datetime
from decimal import Decimal, InvalidOperation


def parse_amount(text):
    """金额字符串 → 整数分。非法输入抛 ValueError。"""
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


def add_record(data, amount_text, note, date_str=None, category="未分类"):
    """新增一笔，返回新记录的 dict。不负责存盘。"""
    if date_str is None:
        date_str = datetime.date.today().isoformat()

    record = {
        "id": next_id(data, date_str),
        "date": date_str,
        "amount_cents": parse_amount(amount_text),
        "note": note,
        "category": category,
    }
    data["records"].append(record)
    return record


def list_records(data, month=None, limit=10):
    """按日期倒序返回记录列表。month 形如 2026-11。"""
    records = data["records"]
    if month:
        records = [r for r in records if r["date"].startswith(month)]
    records = sorted(records, key=lambda r: (r["date"], r["id"]), reverse=True)
    if limit is not None:
        records = records[:limit]
    return records


def summarize(data, month=None):
    """返回 {"total_cents", "count", "by_category"}。"""
    records = list_records(data, month=month, limit=None)

    total = 0
    by_category = {}
    for r in records:
        cents = r["amount_cents"]
        total += cents
        cat = r["category"]
        by_category[cat] = by_category.get(cat, 0) + cents

    return {
        "total_cents": total,
        "count": len(records),
        "by_category": by_category,
    }


def delete_record(data, record_id):
    """删除指定记录并返回它；找不到抛 ValueError。"""
    for index, record in enumerate(data["records"]):
        if record["id"] == record_id:
            return data["records"].pop(index)
    raise ValueError(f"找不到这笔记录：{record_id}")