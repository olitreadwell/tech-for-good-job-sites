#!/usr/bin/env python3
"""Build GUIDE.md and a static searchable site from data/entries/.

Outputs:
    GUIDE.md          - full directory grouped by status and category
    site/index.html   - searchable, filterable single-page site
    site/data.json    - machine-readable copy of the data
    site/data.csv     - flattened copy of the data

Usage:
    python3 scripts/build.py
"""

from __future__ import annotations

import csv
import html
import json
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "data" / "entries"
GUIDE_PATH = ROOT / "GUIDE.md"
SITE_DIR = ROOT / "site"
OUT_HTML = SITE_DIR / "index.html"
OUT_JSON = SITE_DIR / "data.json"
OUT_CSV = SITE_DIR / "data.csv"

STATUS_ORDER = ["live", "blocked", "dead"]
CATEGORY_ORDER = ["job-board", "aggregator", "company-careers", "ats", "resource"]


def load_entries() -> list[dict]:
    entries = []
    for f in sorted(ENTRIES_DIR.glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        data["_file"] = f.name
        entries.append(data)
    return entries


def build_guide(entries: list[dict]) -> str:
    lines = [
        "# Directory",
        "",
        f"Generated {date.today().isoformat()} by `scripts/build.py`. "
        "Edit `data/entries/*.yaml`, not this file.",
        "",
    ]
    counts = {s: sum(1 for e in entries if e["status"] == s) for s in STATUS_ORDER}
    lines.append(f"**{len(entries)} entries**: "
                 f"{counts['live']} live, {counts['blocked']} bot-blocked, {counts['dead']} dead.")
    lines.append("")
    for status in STATUS_ORDER:
        sub = [e for e in entries if e["status"] == status]
        if not sub:
            continue
        lines.append(f"## {status.title()}")
        lines.append("")
        for cat in CATEGORY_ORDER:
            cat_entries = [e for e in sub if e["category"] == cat]
            if not cat_entries:
                continue
            lines.append(f"### {cat}")
            lines.append("")
            for e in sorted(cat_entries, key=lambda x: x["name"]):
                tags = f" (tags: {', '.join(e['tags'])})" if e.get("tags") else ""
                lines.append(f"- [{e['name']}]({e['url']}){tags}")
            lines.append("")
    return "\n".join(lines)


def build_site(entries: list[dict]) -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url", "status", "category", "apply_type", "source", "checked", "tags"])
        writer.writeheader()
        for e in entries:
            writer.writerow({k: e.get(k, "") for k in writer.fieldnames})
    rows = "".join(
        f"<tr data-status=\"{html.escape(e['status'])}\" data-category=\"{html.escape(e['category'])}\" "
        f"data-tags=\"{html.escape(' '.join(e.get('tags', [])))}\">"
        f"<td><a href=\"{html.escape(e['url'])}\">{html.escape(e['name'])}</a></td>"
        f"<td>{html.escape(e['status'])}</td>"
        f"<td>{html.escape(e['category'])}</td>"
        f"<td>{html.escape(e['apply_type'])}</td>"
        f"<td>{html.escape(' '.join(e.get('tags', [])))}</td></tr>"
        for e in entries
    )
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Job site directory</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 60rem; padding: 0 1rem; }}
input, select {{ padding: .4rem; margin-right: .5rem; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
th, td {{ text-align: left; padding: .4rem .6rem; border-bottom: 1px solid #ddd; }}
tr[data-status="dead"] {{ opacity: .5; }}
</style>
</head>
<body>
<h1>Job site directory</h1>
<p>{len(entries)} entries, generated {date.today().isoformat()}</p>
<input id="q" placeholder="Search name or URL…" oninput="filter()">
<select id="status" onchange="filter()">
<option value="">all statuses</option>
<option>live</option><option>blocked</option><option>dead</option>
</select>
<select id="category" onchange="filter()">
<option value="">all categories</option>
<option>job-board</option><option>aggregator</option><option>company-careers</option>
<option>ats</option><option>resource</option>
</select>
<table>
<thead><tr><th>Site</th><th>Status</th><th>Category</th><th>Apply</th><th>Tags</th></tr></thead>
<tbody id="rows">{rows}</tbody>
</table>
<script>
function filter() {{
  const q = document.getElementById('q').value.toLowerCase();
  const s = document.getElementById('status').value;
  const c = document.getElementById('category').value;
  for (const tr of document.querySelectorAll('#rows tr')) {{
    const text = tr.textContent.toLowerCase();
    const ok = (!q || text.includes(q)) && (!s || tr.dataset.status === s) && (!c || tr.dataset.category === c);
    tr.style.display = ok ? '' : 'none';
  }}
}}
</script>
</body>
</html>"""
    OUT_HTML.write_text(html_doc, encoding="utf-8")


def main() -> int:
    entries = load_entries()
    if not entries:
        print("error: no entries found", file=sys.stderr)
        return 1
    GUIDE_PATH.write_text(build_guide(entries), encoding="utf-8")
    build_site(entries)
    print(f"ok: {len(entries)} entries -> GUIDE.md + site/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
