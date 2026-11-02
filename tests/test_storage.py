import pytest

from ledger.storage import EMPTY_LEDGER, load_ledger, save_ledger


def test_load_missing_returns_empty(tmp_path):
    """文件不存在 → 空账本，不报错"""
    path = tmp_path / "ledger.json"
    assert load_ledger(path) == EMPTY_LEDGER


def test_roundtrip(tmp_path):
    """存进去再读出来，内容一致"""
    path = tmp_path / "ledger.json"
    data = {
        "version": 1,
        "records": [
            {
                "id": "20261102-001",
                "date": "2026-11-02",
                "amount_cents": 3500,
                "note": "午餐",
                "category": "吃饭",
            }
        ],
    }
    save_ledger(data, path)
    assert load_ledger(path) == data


def test_bad_json_raises(tmp_path):
    """坏 JSON → ValueError，不能静默吞掉"""
    path = tmp_path / "ledger.json"
    path.write_text("{不是合法JSON", encoding="utf-8")
    with pytest.raises(ValueError):
        load_ledger(path)

def test_missing_records_raises(tmp_path):
    """JSON 合法但缺 records → ValueError"""
    path = tmp_path / "ledger.json"
    path.write_text('{"version": 1}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_ledger(path)