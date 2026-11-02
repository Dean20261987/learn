import pytest

from ledger.cli import main


def test_add_prints_id(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    main(["add", "35", "午餐"], path=path)
    out = capsys.readouterr().out
    assert "已记账" in out
    assert "3500" not in out        # 打印的是 35.00，不是分
    assert "35.00" in out


def test_list_empty(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    main(["list"], path=path)
    assert "还没有记录" in capsys.readouterr().out


def test_list_shows_records(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    main(["add", "35", "午餐"], path=path)
    main(["add", "12.5", "咖啡"], path=path)
    main(["list"], path=path)
    out = capsys.readouterr().out
    assert "午餐" in out
    assert "咖啡" in out
    assert "35.00" in out
    assert "12.50" in out


def test_report_output(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    main(["add", "35", "午餐", "--category", "吃饭"], path=path)
    main(["add", "8", "地铁", "--category", "交通"], path=path)
    main(["report"], path=path)
    out = capsys.readouterr().out
    assert "共 2 笔" in out
    assert "43.00" in out
    assert "吃饭" in out
    assert "交通" in out


def test_delete_missing_exits_1(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    with pytest.raises(SystemExit) as exc:
        main(["delete", "20261102-999"], path=path)
    assert exc.value.code == 1
    assert "找不到" in capsys.readouterr().out


def test_bad_amount_exits_1(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    with pytest.raises(SystemExit) as exc:
        main(["add", "abc", "测试"], path=path)
    assert exc.value.code == 1
    assert "金额格式不对" in capsys.readouterr().out