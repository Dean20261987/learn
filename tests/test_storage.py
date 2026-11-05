import pytest

from ledger.storage import EMPTY_LEDGER, load_ledger, save_ledger


def test_load_missing_returns_empty(tmp_path):
    path = tmp_path / "ledger.json"
    assert load_ledger(path) == EMPTY_LEDGER


def test_roundtrip(tmp_path):
    """合法的 v2 数据：存进去再读出来，一字不差。"""
    path = tmp_path / "ledger.json"
    data = {
        "version": 2,
        "records": [
            {
                "id": "20261102-001",
                "date": "2026-11-02",
                "kind": "expense",
                "amount_cents": -3500,
                "note": "午餐",
                "category": "吃饭",
            }
        ],
    }
    save_ledger(data, path)
    assert load_ledger(path) == data


def test_bad_json_raises(tmp_path):
    path = tmp_path / "ledger.json"
    path.write_text("{不是合法JSON", encoding="utf-8")
    with pytest.raises(ValueError):
        load_ledger(path)


def test_missing_records_raises(tmp_path):
    path = tmp_path / "ledger.json"
    path.write_text('{"version": 2}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_ledger(path)


def test_v1_file_migrated_on_load(tmp_path):
    """v1 文件读进来就是 v2。"""
    path = tmp_path / "ledger.json"
    path.write_text(
        '{"version": 1, "records": [{"id": "x", "date": "2026-11-02", "amount_cents": 3500, "note": "a", "category": "c"}]}',
        encoding="utf-8",
    )
    data = load_ledger(path)
    assert data["version"] == 2
    assert data["records"][0]["kind"] == "expense"
    assert data["records"][0]["amount_cents"] == -3500


def test_v2_missing_kind_is_repaired(tmp_path):
    """版本号写着 v2，但记录缺 kind（手改坏 / 写到一半）——读入时修补。"""
    path = tmp_path / "ledger.json"
    path.write_text(
        '{"version": 2, "records": [{"id": "x", "date": "2026-11-02", "amount_cents": 3500, "note": "a", "category": "c"}]}',
        encoding="utf-8",
    )
    data = load_ledger(path)
    assert data["records"][0]["kind"] == "income"
    assert data["records"][0]["amount_cents"] == 3500