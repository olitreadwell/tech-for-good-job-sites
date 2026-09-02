# Tech-for-Good Job Sites

[![Entries](https://img.shields.io/github/directory-file-count/olitreadwell/tech-for-good-job-sites/data/entries?type=file&extension=yaml&label=entries&color=brightgreen)](GUIDE.md)
[![CI](https://github.com/olitreadwell/tech-for-good-job-sites/actions/workflows/ci.yml/badge.svg)](https://github.com/olitreadwell/tech-for-good-job-sites/actions/workflows/ci.yml)
[![Link check](https://github.com/olitreadwell/tech-for-good-job-sites/actions/workflows/linkcheck.yml/badge.svg)](https://github.com/olitreadwell/tech-for-good-job-sites/actions/workflows/linkcheck.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A living, link-checked directory of tech-for-good job sites — climate, civic, nonprofit, impact, and public-interest roles.

## What this is

A living, link-checked directory of tech-for-good job sites: climate, civic, nonprofit, impact, and public-interest work. Every entry is a small YAML
file with a verified URL, status, category, apply type, source, and tags.
Consolidated and deduplicated from popular community lists, then checked with
[lychee](https://github.com/lycheeverse/lychee).

Current state (checked 2026-09-02):

- **453 live** — reachable and returning 2xx/3xx
- **74 bot-blocked** — site is up but blocks automated checks (403/429)
- **179 dead or unreachable** — 404, 5xx, DNS/TLS errors, or timeout

## Browse it

**[Read the full directory in GUIDE.md](GUIDE.md)** — every entry grouped by
status and category, with facets.

A searchable site is generated from the data by `scripts/build.py` and
deploys to GitHub Pages (see `.github/workflows/pages.yml`). Enable Pages
once, then browse at the repo's Pages URL.

## Facets

Entries carry open-ended `tags`. Currently tagged:

- **Sector** — climate, sustainability, civic, nonprofit, social-impact, justice, human-rights, responsible-tech, government, data
- **Region** — nz, uk
- **Type** — spreadsheet, github-list, social, community

Dedicated facet repos: [4-day-week-job-sites](https://github.com/olitreadwell/4-day-week-job-sites) and [employee-owned-job-sites](https://github.com/olitreadwell/employee-owned-job-sites).
## Use the data

- `data/entries/*.yaml` — one file per site, validated against
  `schema/entry.schema.json`
- `site/data.json` + `site/data.csv` — machine-readable exports (generated)

## How it's maintained

- **Weekly link check** — `.github/workflows/linkcheck.yml` runs lychee over
  all live URLs every Monday NZ time and opens a tracking issue for dead links
- **CI on every push** — `.github/workflows/ci.yml` validates the data and
  rebuilds the site
- **Local checks** — `python3 scripts/validate.py`, `python3 scripts/build.py`,
  `python3 scripts/check.py`

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md). Adding a site is one small YAML file.

## Related

- [remote-job-sites](https://github.com/olitreadwell/remote-job-sites) — general remote job search sites
- [4-day-week-job-sites](https://github.com/olitreadwell/4-day-week-job-sites) — four-day work week job sites
- [employee-owned-job-sites](https://github.com/olitreadwell/employee-owned-job-sites) — employee-owned & cooperative job sites
- [new-zealand-data](https://github.com/olitreadwell/new-zealand-data) — NZ data & APIs directory
