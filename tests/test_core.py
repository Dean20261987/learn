import datetime

import pytest

from ledger.core import (
    add_record,
    delete_record,
    format_cents,
    list_records,
    next_id,
    parse_amount,
    summarize,
    to_export_rows,
    update_record,
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
    data = {"version": 2, "records": []}
    assert next_id(data, "2026-11-02") == "20261102-001"


def test_next_id_increments():
    data = {"version": 2, "records": []}
    add_record(data, "10", "A")
    add_record(data, "20", "B")
    ids = [r["id"] for r in data["records"]]
    assert ids[0].endswith("-001")
    assert ids[1].endswith("-002")
    assert ids[0][:8] == ids[1][:8]


def test_next_id_after_delete():
    data = {
        "version": 2,
        "records": [
            {"id": "20261102-001", "date": "2026-11-02"},
            {"id": "20261102-005", "date": "2026-11-02"},
        ],
    }
    assert next_id(data, "2026-11-02") == "20261102-006"


def _empty():
    return {"version": 2, "records": []}


def test_add_record_fields():
    data = _empty()
    rec = add_record(data, "35", "午餐", date_str="2026-11-02", category="吃饭")
    assert rec["id"].endswith("-001")
    assert rec["date"] == "2026-11-02"
    assert rec["kind"] == "expense"
    assert rec["amount_cents"] == -3500
    assert rec["note"] == "午餐"
    assert rec["category"] == "吃饭"


def test_add_income_positive():
    data = _empty()
    rec = add_record(data, "5000", "工资", date_str="2026-11-02", kind="income", category="工资")
    assert rec["kind"] == "income"
    assert rec["amount_cents"] == 500000


def test_add_rejects_bad_kind():
    with pytest.raises(ValueError):
        add_record(_empty(), "10", "x", kind="other")


def test_add_record_default_date():
    data = _empty()
    rec = add_record(data, "12.5", "咖啡")
    assert rec["date"] == datetime.date.today().isoformat()
    assert rec["kind"] == "expense"
    assert rec["amount_cents"] == -1250
    assert rec["category"] == "未分类"


def test_add_record_appends():
    data = _empty()
    add_record(data, "10", "a", date_str="2026-11-02")
    add_record(data, "20", "b", date_str="2026-11-02")
    assert len(data["records"]) == 2


def test_list_sorted_desc():
    data = _empty()
    add_record(data, "10", "早", date_str="2026-11-01")
    add_record(data, "20", "中", date_str="2026-11-02")
    add_record(data, "30", "晚", date_str="2026-11-02")
    ids = [r["id"] for r in list_records(data)]
    assert ids[0].endswith("-002")
    assert ids[-1].endswith("-001")


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

def test_list_filter_category():
    data = _empty()
    add_record(data, "10", "午餐", date_str="2026-11-02", category="吃饭")
    add_record(data, "20", "地铁", date_str="2026-11-02", category="交通")
    assert len(list_records(data, category="吃饭")) == 1
    assert len(list_records(data, category=None)) == 2

def test_summarize_total():
    data = _empty()
    add_record(data, "35", "午餐", date_str="2026-11-02", category="吃饭")
    add_record(data, "12.5", "咖啡", date_str="2026-11-02", category="吃饭")
    add_record(data, "8", "地铁", date_str="2026-11-02", category="交通")
    s = summarize(data, month="2026-11")
    assert s["count"] == 3
    assert s["expense_cents"] == 5550
    assert s["income_cents"] == 0
    assert s["balance_cents"] == -5550
    assert s["by_category"] == {"吃饭": 4750, "交通": 800}


def test_summarize_mixed():
    data = _empty()
    add_record(data, "35", "午餐", date_str="2026-11-02", category="吃饭")
    add_record(data, "5000", "工资", date_str="2026-11-02", kind="income", category="工资")
    s = summarize(data, month="2026-11")
    assert s["expense_cents"] == 3500
    assert s["income_cents"] == 500000
    assert s["balance_cents"] == 496500
    assert s["by_category"] == {"吃饭": 3500}


def test_summarize_empty():
    s = summarize(_empty())
    assert s == {
        "count": 0,
        "expense_cents": 0,
        "income_cents": 0,
        "balance_cents": 0,
        "by_category": {},
    }


def test_delete_ok():
    data = _empty()
    add_record(data, "10", "a", date_str="2026-11-02")
    add_record(data, "20", "b", date_str="2026-11-02")
    deleted = delete_record(data, data["records"][0]["id"])
    assert deleted["note"] == "a"
    assert len(data["records"]) == 1


def test_delete_missing():
    with pytest.raises(ValueError):
        delete_record(_empty(), "20261102-999")

# ---------- 修改 ----------

def test_update_changes_note():
    """只改说明：金额和类型都不动。"""
    data = _empty()
    rec = add_record(data, "35", "午餐", date_str="2026-11-02", category="吃饭")
    update_record(data, rec["id"], note="午饭加饮料")
    assert rec["note"] == "午饭加饮料"
    assert rec["amount_cents"] == -3500
    assert rec["kind"] == "expense"


def test_update_amount_uses_existing_kind():
    """只改金额：符号按现有类型。"""
    data = _empty()
    rec = add_record(data, "35", "午餐", date_str="2026-11-02")
    update_record(data, rec["id"], amount_text="50")
    assert rec["amount_cents"] == -5000


def test_update_kind_flips_sign():
    """只改类型：绝对值不变，符号翻。"""
    data = _empty()
    rec = add_record(data, "35", "午餐", date_str="2026-11-02")
    update_record(data, rec["id"], kind="income")
    assert rec["kind"] == "income"
    assert rec["amount_cents"] == 3500


def test_update_amount_and_kind():
    """金额和类型一起改：按新类型算符号。"""
    data = _empty()
    rec = add_record(data, "35", "午餐", date_str="2026-11-02")
    update_record(data, rec["id"], amount_text="99", kind="income")
    assert rec["kind"] == "income"
    assert rec["amount_cents"] == 9900


def test_update_can_clear_note():
    """空字符串是合法输入，能把备注清空。"""
    data = _empty()
    rec = add_record(data, "35", "午餐", date_str="2026-11-02")
    update_record(data, rec["id"], note="")
    assert rec["note"] == ""


def test_update_missing_raises():
    with pytest.raises(ValueError):
        update_record(_empty(), "20261102-999", note="x")


def test_update_rejects_bad_kind():
    data = _empty()
    rec = add_record(data, "35", "午餐", date_str="2026-11-02")
    with pytest.raises(ValueError):
        update_record(data, rec["id"], kind="other")

# ---------- 导出 ----------

def test_to_export_rows_header():
    rows = to_export_rows(_empty())
    assert rows == [["单号", "日期", "类型", "金额(元)", "分类", "说明"]]


def test_to_export_rows_amount_format():
    data = _empty()
    add_record(data, "35", "午餐", date_str="2026-11-02", category="吃饭")
    add_record(data, "5000", "工资", date_str="2026-11-02", kind="income")
    rows = to_export_rows(data)
    amounts = {row[0]: row[3] for row in rows[1:]}
    assert set(amounts.values()) == {"-35.00", "5000.00"}


def test_to_export_rows_month_filter():
    data = _empty()
    add_record(data, "10", "十月", date_str="2026-10-30")
    add_record(data, "20", "十一月", date_str="2026-11-02")
    rows = to_export_rows(data, month="2026-11")
    assert len(rows) == 2         # 表头 + 1 行