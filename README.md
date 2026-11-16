# Tech-for-Good Job Sites

[![Entries](https://img.shields.io/github/directory-file-count/olitreadwell/tech-for-good-job-sites/data/entries?type=file&extension=yaml&label=entries&color=brightgreen)](GUIDE.md)
[![Checks](https://github.com/olitreadwell/tech-for-good-job-sites/actions/workflows/ci.yml/badge.svg)](https://github.com/olitreadwell/tech-for-good-job-sites/actions/workflows/ci.yml)
[![Link check](https://github.com/olitreadwell/tech-for-good-job-sites/actions/workflows/linkcheck.yml/badge.svg)](https://github.com/olitreadwell/tech-for-good-job-sites/actions/workflows/linkcheck.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A checked list of tech-for-good job sites. It covers climate, civic, nonprofit, impact, and public-interest roles.

## What this is

This is a checked list of tech-for-good job sites. It covers climate, civic, nonprofit, impact, and public-interest work. Every entry is a small yaml file. It has a verified URL, status, category, apply type, source, and tags.

The sites come from popular community lists. Every link is checked with [lychee](https://github.com/lycheeverse/lychee).

Current state (checked 2026-09-02):

- **326 live**: reachable and returning 2xx/3xx
- **18 bot-blocked**: site is up but blocks automated checks (403/429)
- **42 dead or unreachable**: 404, 5xx, domain lookup or secure connection errors, or timeout

## Browse it

**Read the full directory in <a href="GUIDE.md">the guide</a>**: every entry grouped by
status and category, with facets.

A searchable site is generated from the data by `scripts/build.py` and
deploys to GitHub Pages (see `.github/workflows/pages.yml`). Enable Pages
once, then browse at the repo's Pages URL.

## Facets

Entries carry open-ended `tags`. Currently tagged:

- **Sector**: climate, sustainability, civic, nonprofit, social-impact, justice, human-rights, responsible-tech, government, data
- **Region**: uk
- **Type**: spreadsheet, github-list, social

Dedicated facet repos: [4-day-week-job-sites](https://github.com/olitreadwell/4-day-week-job-sites) and [employee-owned-job-sites](https://github.com/olitreadwell/employee-owned-job-sites).

## Use the data

- `data/entries/*.yaml`: one file per site, validated against
  `schema/entry.schema.json`
- `site/data.json` + `site/data.csv`: machine-readable exports (generated)

## How it is maintained

- **Weekly link check**: `.github/workflows/linkcheck.yml` runs lychee over
  all live URLs every Monday New Zealand time and opens a tracking issue for dead links
- **Automated checks on every push**: `.github/workflows/ci.yml` validates the data and
  rebuilds the site
- **Local checks**: `python3 scripts/validate.py`, `python3 scripts/build.py`,
  `python3 scripts/check.py`

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md). Adding a site is one small yaml file.

## Related

- [remote-job-sites](https://github.com/olitreadwell/remote-job-sites): general remote job search sites
- [4-day-week-job-sites](https://github.com/olitreadwell/4-day-week-job-sites): four-day work week job sites
- [employee-owned-job-sites](https://github.com/olitreadwell/employee-owned-job-sites): employee-owned & cooperative job sites
- [new-zealand-data](https://github.com/olitreadwell/new-zealand-data): NZ data & APIs directory
