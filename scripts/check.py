#!/usr/bin/env python3
"""Link-check all live entries with lychee.

Extracts live URLs from data/entries/, writes them to a temp file, and runs
lychee over them. Bot-blocked responses (403/429) are accepted, not failures.

Usage:
    python3 scripts/check.py [--accept 200,201,301,302,403,429]
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "data" / "entries"
DEFAULT_ACCEPT = (
    "200,201,202,203,204,206,301,302,303,307,308,"
    "400,401,402,403,405,406,423,429,999"
)
FALLBACK_ACCEPT = set(range(200, 400)) | {400, 401, 402, 403, 405, 406, 423, 429, 999}
FAILURE_LINE = re.compile(r"^\[(?:ERROR|TIMEOUT|\d{3})\]\s+(\S+)")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def live_urls() -> list[str]:
    urls = []
    for f in sorted(ENTRIES_DIR.glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        if data.get("status") == "live":
            urls.append(data["url"])
    return urls


def failed_urls(*outputs: str) -> set[str]:
    """Extract URLs from lychee failure lines across stdout and stderr."""
    return {
        match.group(1)
        for output in outputs
        for line in output.splitlines()
        if (match := FAILURE_LINE.match(line))
    }


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
        "--max-concurrency", "16",
        "--timeout", "30",
        "--user-agent", USER_AGENT,
        tmp,
    ]
    print(f"checking {len(urls)} live URLs with lychee…")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode == 0:
        return 0

    failed = sorted(failed_urls(result.stdout, result.stderr))
    if not failed:
        print("error: lychee failed without parseable failures", file=sys.stderr)
        return 1
    remaining = []
    for url in failed:
        status = fallback_status(url)
        if status in FALLBACK_ACCEPT:
            print(f"fallback ok: {url} ({status})")
        else:
            print(f"still failing: {url} ({status or 'no response'})")
            remaining.append(url)
    return 0 if not remaining else 1


def fallback_status(url: str) -> int | None:
    """Retry one URL over HTTP/1.1 so transient HTTP/2 and timeout failures do not fail the gate."""
    result = subprocess.run(
        [
            "curl",
            "--http1.1",
            "-L",
            "-sS",
            "-o",
            "/dev/null",
            "-w",
            "%{http_code}",
            "--max-time",
            "45",
            "-A",
            USER_AGENT,
            url,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    try:
        return int(result.stdout.strip())
    except ValueError:
        return None


if __name__ == "__main__":
    sys.exit(main())
