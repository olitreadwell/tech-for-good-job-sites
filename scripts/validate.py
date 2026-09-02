#!/usr/bin/env python3
"""Validate every entry in data/entries/ against the schema rules.

Pure stdlib + PyYAML. Exits non-zero on any problem. Run in CI and locally.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "data" / "entries"

STATUSES = {"live", "blocked", "dead"}
CATEGORIES = {"job-board", "aggregator", "company-careers", "ats", "resource"}
APPLY_TYPES = {"quick", "ats", "unknown"}
REQUIRED = {"name", "url", "status", "category", "apply_type", "source", "checked"}
URL_RE = re.compile(r"^https?://[^\s]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_entry(path: Path, seen_urls: set[str]) -> list[str]:
    errors = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"{path.name}: invalid YAML: {e}"]
    if not isinstance(data, dict):
        return [f"{path.name}: entry must be a mapping"]

    for field in REQUIRED:
        if field not in data:
            errors.append(f"{path.name}: missing required field '{field}'")
    if "name" in data and not isinstance(data["name"], str):
        errors.append(f"{path.name}: 'name' must be a string")
    if "url" in data:
        if not isinstance(data["url"], str) or not URL_RE.match(data["url"]):
            errors.append(f"{path.name}: 'url' must be an http(s) URL")
        else:
            if data["url"] in seen_urls:
                errors.append(f"{path.name}: duplicate url {data['url']}")
            seen_urls.add(data["url"])
    if "status" in data and data["status"] not in STATUSES:
        errors.append(f"{path.name}: bad status '{data['status']}'")
    if "category" in data and data["category"] not in CATEGORIES:
        errors.append(f"{path.name}: bad category '{data['category']}'")
    if "apply_type" in data and data["apply_type"] not in APPLY_TYPES:
        errors.append(f"{path.name}: bad apply_type '{data['apply_type']}'")
    if "checked" in data and not DATE_RE.match(str(data["checked"])):
        errors.append(f"{path.name}: 'checked' must be YYYY-MM-DD")
    if "source" in data:
        srcs = data["source"] if isinstance(data["source"], list) else [data["source"]]
        if not srcs or not all(isinstance(s, str) and s for s in srcs):
            errors.append(f"{path.name}: 'source' must be a non-empty list of strings")
    if "tags" in data and not isinstance(data["tags"], list):
        errors.append(f"{path.name}: 'tags' must be a list")
    return errors


def main() -> int:
    if not ENTRIES_DIR.is_dir():
        print(f"error: {ENTRIES_DIR} not found", file=sys.stderr)
        return 1
    files = sorted(ENTRIES_DIR.glob("*.yaml"))
    if not files:
        print("error: no entries found", file=sys.stderr)
        return 1
    seen_urls: set[str] = set()
    all_errors: list[str] = []
    for f in files:
        all_errors.extend(validate_entry(f, seen_urls))
    if all_errors:
        for e in all_errors:
            print(f"error: {e}", file=sys.stderr)
        print(f"{len(all_errors)} problem(s) across {len(files)} entries", file=sys.stderr)
        return 1
    print(f"ok: {len(files)} entries valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
