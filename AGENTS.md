# Agent instructions

This repo is a data directory. The data is the product; the code is tooling
around it.

## Ground rules

- Every site lives in `data/entries/<slug>.yaml`. One file per site.
- Every entry must pass `python3 scripts/validate.py` (schema in
  `schema/entry.schema.json`).
- Never invent a URL, status, or source. If a site can't be verified, mark it
  `status: dead` or leave it out.
- `status` values: `live` (2xx/3xx), `blocked` (site up, bot-blocked 403/429),
  `dead` (404, 5xx, DNS/TLS, timeout).
- `category` values: `job-board`, `aggregator`, `company-careers`, `ats`,
  `resource`.
- `apply_type` values: `quick` (one-click/email apply), `ats` (application
  form), `unknown`.
- `tags` are open-ended. Reuse existing tags before inventing new ones.
- `source` lists which upstream list(s) contributed the URL. Use the repo
  name, or `user` for direct additions.
- `checked` is the ISO date the URL was last link-checked.

## Workflow

1. Add or edit `data/entries/<slug>.yaml`.
2. Run `python3 scripts/validate.py`: must pass.
3. Run `python3 scripts/dedupe.py`: prints entries that repeat a host; `--apply` deletes them. One entry per host.
4. Run `python3 scripts/check.py`: confirms live URLs still resolve.
5. Run `python3 scripts/build.py`: regenerates `GUIDE.md` and `site/`.
6. Commit data + regenerated outputs together.

## Naming

- Slug = host, then path words, hyphenated (`remoteok-io.yaml`,
  `boards-greenhouse-io-carbonchain.yaml`).
- `name` = the site's host (e.g. `remoteok.io`), not a marketing name, unless
  the marketing name is unambiguous.
