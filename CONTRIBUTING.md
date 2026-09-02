# Contributing

Thanks for helping keep this directory alive. Two ways to contribute:

## Add a site

1. Check it's not already in `data/entries/` (search by host).
2. Create `data/entries/<slug>.yaml`:

```yaml
name: example.com
url: https://example.com/
status: live
category: job-board
apply_type: quick
source: [awesome-remote-job]
checked: '2026-09-02'
tags: [4-day-week]
```

3. Run the checks:

```bash
python3 scripts/validate.py
python3 scripts/check.py
python3 scripts/build.py
```

4. Open a PR with the entry + regenerated `GUIDE.md`/`site/`.

## Report a dead link

Open an issue with the URL. The weekly link check also tracks dead links
automatically.

## Field reference

| Field | Values |
| --- | --- |
| `status` | `live`, `blocked`, `dead` |
| `category` | `job-board`, `aggregator`, `company-careers`, `ats`, `resource` |
| `apply_type` | `quick`, `ats`, `unknown` |
| `tags` | open-ended; reuse existing (`4-day-week`, `employee-owned`, `cooperative`, ...) |
| `source` | upstream list repo name, or `user` |
| `checked` | ISO date of last link check |
