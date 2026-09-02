"""Data integrity tests. Run with: pytest"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "data" / "entries"
SCHEMA = ROOT / "schema" / "entry.schema.json"

STATUSES = {"live", "blocked", "dead"}
CATEGORIES = {"job-board", "aggregator", "company-careers", "ats", "resource"}
APPLY_TYPES = {"quick", "ats", "unknown"}
REQUIRED = {"name", "url", "status", "category", "apply_type", "source", "checked"}


def load_entries():
    return [yaml.safe_load(f.read_text(encoding="utf-8")) for f in ENTRIES_DIR.glob("*.yaml")]


def test_entries_exist():
    assert len(list(ENTRIES_DIR.glob("*.yaml"))) > 0


def test_schema_exists():
    assert SCHEMA.is_file()


def test_required_fields():
    for e in load_entries():
        assert REQUIRED <= set(e), f"missing fields in {e.get('name')}"


def test_enums():
    for e in load_entries():
        assert e["status"] in STATUSES
        assert e["category"] in CATEGORIES
        assert e["apply_type"] in APPLY_TYPES


def test_urls_unique():
    urls = [e["url"] for e in load_entries()]
    assert len(urls) == len(set(urls))


def test_urls_are_http():
    for e in load_entries():
        assert e["url"].startswith(("http://", "https://"))
