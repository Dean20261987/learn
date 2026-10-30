import pytest

from mypkg.logstat import analyze_log


def test_counts_errors(tmp_path):
    log = tmp_path / "a.log"
    log.write_text(
        "2026-10-30 09:00:00 INFO  启动\n"
        "2026-10-30 09:00:01 ERROR 数据库连接失败\n"
        "2026-10-30 09:00:02 ERROR 权限不足\n"
        "2026-10-30 09:00:03 ERROR 数据库连接失败\n",
        encoding="utf-8",
    )
    assert analyze_log(log) == {"数据库连接失败": 2, "权限不足": 1}


def test_no_errors(tmp_path):
    log = tmp_path / "b.log"
    log.write_text("2026-10-30 09:00:00 INFO 一切正常\n", encoding="utf-8")
    assert analyze_log(log) == {}


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        analyze_log(tmp_path / "没有这个日志.log")