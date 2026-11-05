import pytest

from ledger.cli import main
from ledger.storage import load_ledger


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

def test_edit_changes_note(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    main(["add", "35", "午餐"], path=path)
    capsys.readouterr()

    record_id = load_ledger(path)["records"][0]["id"]
    main(["edit", record_id, "--note", "新说明"], path=path)

    out = capsys.readouterr().out
    assert "已修改" in out
    assert "新说明" in out


def test_edit_missing_exits_1(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    with pytest.raises(SystemExit) as exc:
        main(["edit", "20991111-999", "--note", "x"], path=path)
    assert exc.value.code == 1
    assert "找不到" in capsys.readouterr().out

def test_report_shows_percentage(tmp_path, capsys):
    """两个分类，百分比应该对得上。"""
    path = tmp_path / "ledger.json"
    main(["add", "30", "午餐", "--category", "吃饭"], path=path)
    main(["add", "10", "地铁", "--category", "交通"], path=path)
    main(["report"], path=path)
    out = capsys.readouterr().out
    assert "75.0%" in out          # 30/40
    assert "25.0%" in out          # 10/40


def test_report_only_income_no_category(tmp_path, capsys):
    """只有收入时不崩，也不打印分类行。"""
    path = tmp_path / "ledger.json"
    main(["add", "5000", "工资", "--income"], path=path)
    main(["report"], path=path)
    out = capsys.readouterr().out
    assert "支出分类" not in out
    assert "100.0%" not in out


def test_report_month_filter(tmp_path, capsys):
    """--month 只统计该月。"""
    path = tmp_path / "ledger.json"
    main(["add", "10", "十月", "--date", "2026-10-30"], path=path)
    main(["add", "20", "十一月", "--date", "2026-11-02"], path=path)
    capsys.readouterr()                       # ← 清掉 add 的输出

    main(["report", "--month", "2026-11"], path=path)
    out = capsys.readouterr().out
    assert "共 1 笔" in out
    assert "20.00" in out
    assert "10.00" not in out


def test_list_filter_category(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    main(["add", "30", "午餐", "--category", "吃饭"], path=path)
    main(["add", "10", "地铁", "--category", "交通"], path=path)
    capsys.readouterr()                       # ← 清掉 add 的输出

    main(["list", "--category", "吃饭"], path=path)
    out = capsys.readouterr().out
    assert "午餐" in out
    assert "地铁" not in out

def test_export_writes_csv(tmp_path, capsys):
    path = tmp_path / "ledger.json"
    main(["add", "35", "午餐", "--category", "吃饭"], path=path)
    capsys.readouterr()

    out_file = tmp_path / "账单.csv"
    main(["export", str(out_file)], path=path)
    assert "已导出 1 条" in capsys.readouterr().out

    text = out_file.read_text(encoding="utf-8-sig")
    assert "单号" in text
    assert "午餐" in text
    assert "-35.00" in text


def test_export_has_bom(tmp_path):
    """确认写的是 utf-8-sig（否则 Excel 打开中文乱码）。"""
    path = tmp_path / "ledger.json"
    main(["add", "10", "测试"], path=path)
    out_file = tmp_path / "out.csv"
    main(["export", str(out_file)], path=path)

    assert out_file.read_bytes()[:3] == b"\xef\xbb\xbf"