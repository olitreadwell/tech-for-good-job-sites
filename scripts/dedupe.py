#!/usr/bin/env python3
"""Keep one entry per host, dropping the same site listed several times.

A directory of job sites should show each site once. Upstream lists supply
the company home page and its careers page, or several tenant pages on one
board host, and every copy renders as the same name.

Pass --check to see what would go, --apply to delete the duplicates. The
kept entry is the one that is live, points at a jobs or careers page, and
sits closest to the root.
"""

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "data" / "entries"

JOBS_SEGMENT_STARTS = {
    "apply",
    "career",
    "careers",
    "emplois",
    "employ",
    "hiring",
    "job",
    "jobs",
    "join",
    "karriere",
    "offene",
    "openings",
    "recruit",
    "recruiting",
    "stellen",
    "vacancies",
    "vacancy",
    "vacatures",
    "vacature",
    "werk",
    "work",
}


def starts_with_jobs_word(path: str) -> bool:
    """Say whether the first path segment is a jobs or careers page.

    `job-board` and `offene_stellen` count. `remote-engineering-jobs` does
    not: it is a filter on a board, not the board.
    """
    segment = path.strip("/").split("/")[0]
    first = re.split(r"[-_.]", segment)[0].lower()
    return first in JOBS_SEGMENT_STARTS
STATUS_RANK = {"live": 3, "blocked": 2, "dead": 1}


def host_and_path(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.rstrip("/") or "/"
    return host, path


def path_rank(path: str) -> int:
    """Rank a path for a directory of sites.

    A shallow jobs or careers page beats a company home page, and a home
    page beats a deeper filter page on the same board, so 4dayweek.io keeps
    its root and a company keeps its /careers page.
    """
    depth = path.count("/")
    if path == "/":
        return 1
    if depth == 1 and starts_with_jobs_word(path):
        return 2
    return 0


def score(entry: dict) -> tuple:
    _, path = host_and_path(entry["url"])
    return (
        STATUS_RANK.get(entry.get("status", ""), 0),
        path_rank(path),
        -path.count("/"),
        -len(entry["url"]),
    )


def load() -> list[dict]:
    out = []
    for path in sorted(ENTRIES_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["_path"] = path
        out.append(data)
    return out


def plan(entries: list[dict]) -> tuple[dict[str, dict], list[dict]]:
    by_host: dict[str, list[dict]] = {}
    for entry in entries:
        host, _ = host_and_path(entry["url"])
        by_host.setdefault(host, []).append(entry)
    keep: dict[str, dict] = {}
    drop: list[dict] = []
    for host, group in by_host.items():
        kept = max(sorted(group, key=lambda e: str(e["_path"])), key=score)
        keep[host] = kept
        drop.extend(entry for entry in group if entry is not kept)
    return keep, drop


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="delete the duplicates")
    args = parser.parse_args()

    entries = load()
    keep, drop = plan(entries)
    print(f"{len(entries)} entries, {len(keep)} hosts, {len(drop)} duplicates")
    for entry in drop[:10]:
        print(f"  drop {entry['_path'].name}  {entry['url']}")
    if not args.apply:
        print("dry run, pass --apply to delete")
        return 0
    for entry in drop:
        entry["_path"].unlink()
    print(f"deleted {len(drop)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
