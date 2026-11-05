from ledger.storage import CURRENT_VERSION, migrate


def test_migrate_v1_adds_kind():
    data = {
        "version": 1,
        "records": [{"id": "x", "date": "2026-11-02", "amount_cents": 3500}],
    }
    result = migrate(data)
    assert result["version"] == 2
    assert result["records"][0]["kind"] == "expense"
    assert result["records"][0]["amount_cents"] == -3500


def test_migrate_keeps_income_positive():
    data = {
        "version": 1,
        "records": [{"id": "x", "kind": "income", "amount_cents": 5000}],
    }
    result = migrate(data)
    assert result["records"][0]["kind"] == "income"
    assert result["records"][0]["amount_cents"] == 5000


def test_migrate_fixes_income_sign():
    data = {"version": 1, "records": [{"id": "x", "kind": "income", "amount_cents": -5000}]}
    result = migrate(data)
    assert result["records"][0]["amount_cents"] == 5000


def test_migrate_v2_legal_untouched():
    """合法的 v2 数据跑一遍，什么都不变（幂等）。"""
    data = {
        "version": 2,
        "records": [
            {"id": "a", "kind": "expense", "amount_cents": -3500},
            {"id": "b", "kind": "income", "amount_cents": 5000},
        ],
    }
    before = [dict(r) for r in data["records"]]
    result = migrate(data)
    assert result["records"] == before


def test_migrate_v2_missing_kind_repaired():
    """版本号是 v2 但缺 kind —— 也要补上（不能信任版本号）。"""
    data = {"version": 2, "records": [{"id": "x", "amount_cents": 3500}]}
    result = migrate(data)
    assert result["records"][0]["kind"] == "income"
    assert result["records"][0]["amount_cents"] == 3500


def test_migrate_empty_records():
    data = {"version": 1, "records": []}
    result = migrate(data)
    assert result["version"] == 2
    assert result["records"] == []


def test_migrate_missing_version():
    data = {"records": [{"id": "x", "amount_cents": 100}]}
    result = migrate(data)
    assert result["version"] == 2
    assert result["records"][0]["kind"] == "expense"
    assert result["records"][0]["amount_cents"] == -100


def test_current_version_is_two():
    assert CURRENT_VERSION == 2