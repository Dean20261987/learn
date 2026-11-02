import datetime

import pytest

from ledger.core import (
    add_record,
    delete_record,
    list_records,
    next_id,
    parse_amount,
    summarize,
)


@pytest.mark.parametrize("text, expected", [
    ("35", 3500),
    ("12.5", 1250),
    ("12.50", 1250),
    ("0.01", 1),
    ("100", 10000),
    ("35.0", 3500),
])
def test_parse_amount_ok(text, expected):
    assert parse_amount(text) == expected


@pytest.mark.parametrize("text", ["0", "-5", "abc", "", "12.555"])
def test_parse_amount_invalid(text):
    with pytest.raises(ValueError):
        parse_amount(text)


def test_next_id_empty():
    data = {"version": 1, "records": []}
    assert next_id(data, "2026-11-02") == "20261102-001"


def test_next_id_increments():
    data = {
        "version": 1,
        "records": [
            {"id": "20261102-001", "date": "2026-11-02"},
            {"id": "20261102-002", "date": "2026-11-02"},
            {"id": "20261101-001", "date": "2026-11-01"},
        ],
    }
    assert next_id(data, "2026-11-02") == "20261102-003"


def test_next_id_after_delete():
    data = {
        "version": 1,
        "records": [
            {"id": "20261102-001", "date": "2026-11-02"},
            {"id": "20261102-005", "date": "2026-11-02"},
        ],
    }
    assert next_id(data, "2026-11-02") == "20261102-006"


def _empty():
    return {"version": 1, "records": []}


def test_add_record_fields():
    data = _empty()
    rec = add_record(data, "35", "午餐", date_str="2026-11-02", category="吃饭")
    assert rec["id"] == "20261102-001"
    assert rec["date"] == "2026-11-02"
    assert rec["amount_cents"] == 3500
    assert rec["note"] == "午餐"
    assert rec["category"] == "吃饭"


def test_add_record_default_date():
    data = _empty()
    rec = add_record(data, "12.5", "咖啡")
    assert rec["date"] == datetime.date.today().isoformat()
    assert rec["amount_cents"] == 1250
    assert rec["category"] == "未分类"


def test_add_record_appends():
    data = _empty()
    add_record(data, "10", "a", date_str="2026-11-02")
    add_record(data, "20", "b", date_str="2026-11-02")
    assert len(data["records"]) == 2
    assert data["records"][1]["id"] == "20261102-002"


def test_list_sorted_desc():
    data = _empty()
    add_record(data, "10", "早", date_str="2026-11-01")
    add_record(data, "20", "中", date_str="2026-11-02")
    add_record(data, "30", "晚", date_str="2026-11-02")
    ids = [r["id"] for r in list_records(data)]
    assert ids == ["20261102-002", "20261102-001", "20261101-001"]


def test_list_filter_month():
    data = _empty()
    add_record(data, "10", "十月", date_str="2026-10-30")
    add_record(data, "20", "十一月", date_str="2026-11-02")
    assert len(list_records(data, month="2026-11")) == 1


def test_list_limit():
    data = _empty()
    for i in range(5):
        add_record(data, "10", f"第{i}笔", date_str="2026-11-02")
    assert len(list_records(data, limit=2)) == 2
    assert len(list_records(data, limit=None)) == 5


def test_summarize_total():
    data = _empty()
    add_record(data, "35", "午餐", date_str="2026-11-02", category="吃饭")
    add_record(data, "12.5", "咖啡", date_str="2026-11-02", category="吃饭")
    add_record(data, "8", "地铁", date_str="2026-11-02", category="交通")
    s = summarize(data, month="2026-11")
    assert s["total_cents"] == 5550
    assert s["count"] == 3
    assert s["by_category"] == {"吃饭": 4750, "交通": 800}


def test_summarize_empty():
    data = _empty()
    s = summarize(data)
    assert s == {"total_cents": 0, "count": 0, "by_category": {}}


def test_delete_ok():
    data = _empty()
    add_record(data, "10", "a", date_str="2026-11-02")
    add_record(data, "20", "b", date_str="2026-11-02")
    deleted = delete_record(data, "20261102-001")
    assert deleted["note"] == "a"
    assert len(data["records"]) == 1


def test_delete_missing():
    data = _empty()
    with pytest.raises(ValueError):
        delete_record(data, "20261102-999")