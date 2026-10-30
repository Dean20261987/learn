import json

import pytest

from mypkg.notes import load_notes


def test_bad_json_raises(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{不是合法JSON", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_notes(p)

from mypkg.notes import load_notes, save_notes


def test_roundtrip(tmp_path):
    path = tmp_path / "notes.json"
    data = {"2026-10-30": "第7周开工"}
    save_notes(data, path)
    assert load_notes(path) == data


def test_missing_file(tmp_path):
    assert load_notes(tmp_path / "没有这个文件.json") == {}