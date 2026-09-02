#!/usr/bin/env python3
"""Link-check all live entries with lychee.

Extracts live URLs from data/entries/, writes them to a temp file, and runs
lychee over them. Bot-blocked responses (403/429) are accepted, not failures.

Usage:
    python3 scripts/check.py [--accept 200,201,301,302,403,429]
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "data" / "entries"
DEFAULT_ACCEPT = "200,201,202,203,204,206,301,302,303,307,308,403,429,999"


def live_urls() -> list[str]:
    urls = []
    for f in sorted(ENTRIES_DIR.glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        if data.get("status") == "live":
            urls.append(data["url"])
    return urls


def main() -> int:
    accept = DEFAULT_ACCEPT
    if "--accept" in sys.argv:
        i = sys.argv.index("--accept")
        accept = sys.argv[i + 1]
    urls = live_urls()
    if not urls:
        print("error: no live entries found", file=sys.stderr)
        return 1
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("\n".join(urls) + "\n")
        tmp = f.name
    cmd = [
        "lychee",
        "--accept", accept,
        "--no-progress",
        "--max-concurrency", "64",
        "--timeout", "15",
        "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        tmp,
    ]
    print(f"checking {len(urls)} live URLs with lychee…")
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
