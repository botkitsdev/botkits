"""Tests for csv_page.py. Run: python3 -m pytest -q skills/youtube/botkits-channel-performance-page/scripts"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import csv_page as cp  # noqa: E402

EXAMPLE = HERE.parent / "example" / "studio-export.csv"


def test_parse_num_handles_studio_formats():
    assert cp.parse_num("1,234") == 1234
    assert cp.parse_num("1.2K") == 1200
    assert cp.parse_num("3.9%") == 3.9
    assert cp.parse_num("2M") == 2_000_000
    assert cp.parse_num("") is None and cp.parse_num("—") is None


def test_parse_seconds():
    assert cp.parse_seconds("0:01:19") == 79
    assert cp.parse_seconds("1:19") == 79
    assert cp.parse_seconds("742") == 742


def test_example_reads_total_row_and_splits_types():
    rows, total, gaps = cp.read_export(EXAMPLE)
    assert len(rows) == 8 and total["views"] == 18412
    assert sum(r["type"] == "short" for r in rows) == 5
    assert gaps == []


def test_build_bands_stars_and_losers():
    rows, total, gaps = cp.read_export(EXAMPLE)
    d = cp.build(rows, total, gaps, "Sample")
    assert [s["b"] for s in d["stayed"]] == ["hi", "hi", "mid", "mid", "lo"]
    assert d["stayed"][-1]["new"] is False  # 20 Nov is more than 7 days before 27 Nov
    assert d["wins"][0]["v"] == "6,204 views"
    assert any("stayed" in l["v"] for l in d["loses"])


def test_missing_columns_become_gaps_not_errors(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("Video title,Views\nA,1.2K\nB,30\n", encoding="utf-8")
    rows, total, gaps = cp.read_export(p)
    assert rows[0]["views"] == 1200
    assert "no % stayed column" in gaps and any("rounded" in g for g in gaps)
    page = cp.render(cp.build(rows, total, gaps, "X"))
    assert "<!doctype html>" in page and "/*{{DATA}}*/" not in page


def test_title_is_escaped_and_script_cannot_break_out(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text('Video title,Views\n"</script><b>x",10\n', encoding="utf-8")
    rows, total, gaps = cp.read_export(p)
    page = cp.render(cp.build(rows, total, gaps, "X", title="<i>t</i>"))
    assert "</script><b>" not in page and "<i>t</i>" not in page


def test_cli_writes_page_and_json(tmp_path):
    out, js = tmp_path / "p.html", tmp_path / "p.json"
    assert cp.main([str(EXAMPLE), "--out", str(out), "--json", str(js), "--channel", "Sample"]) == 0
    assert re.search(r"<title>.+</title>", out.read_text())
    assert json.loads(js.read_text())["channel"] == "Sample"
