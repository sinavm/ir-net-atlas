<div align="center">

# IR Net Atlas

### Iran Internet Reachability Observatory

An open, continuously updated observatory for tracking the reachability of public websites and services related to Iran's internet ecosystem.

<p>
  <a href="https://github.com/sinavm/ir-net-atlas/stargazers"><img src="https://img.shields.io/github/stars/sinavm/ir-net-atlas?style=for-the-badge&logo=github&color=f59e0b&label=Star%20on%20GitHub" alt="Star on GitHub"></a>
  <a href="https://sinavm.github.io/ir-net-atlas/"><img src="https://img.shields.io/badge/OPEN-LIVE%20ATLAS-0891b2?style=for-the-badge&logo=githubpages&logoColor=white" alt="Open Live Atlas"></a>
</p>

<p>
  <a href="https://github.com/sinavm/ir-net-atlas/actions/workflows/probe.yml"><img src="https://img.shields.io/github/actions/workflow/status/sinavm/ir-net-atlas/probe.yml?branch=main&style=flat-square&label=Probe%20workflow" alt="Probe workflow"></a>
  <a href="https://github.com/sinavm/ir-net-atlas/commits/main"><img src="https://img.shields.io/github/last-commit/sinavm/ir-net-atlas?style=flat-square&color=64748b" alt="Last commit"></a>
  <a href="https://github.com/sinavm/ir-net-atlas/blob/main/LICENSE"><img src="https://img.shields.io/github/license/sinavm/ir-net-atlas?style=flat-square&color=10b981" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/status-open%20data-0d9488?style=flat-square" alt="Open data">
</p>

<p>
  <a href="https://sinavm.github.io/ir-net-atlas/"><img src="https://raw.githubusercontent.com/sinavm/ir-net-atlas/main/docs/badge.svg" alt="Current Atlas status"></a>
</p>

</div>

---

## Overview

**IR Net Atlas** collects and publishes network reachability measurements to make internet disruptions and service availability easier to observe over time.

The project keeps measurement perspectives separate instead of treating a single probe as a complete picture:

- **External probes** — GitHub Actions checks a curated set of Iranian websites and public API endpoints from GitHub-hosted runners outside Iran.
- **In-country observations** — the collector attempts to retrieve public measurements from ArvanCloud Radar, with OONI measurements as a fallback when available.
- **International service targets** — a separate curated target list is published for the Atlas dashboard's browser-side checks.

> **Important:** A successful or failed check from GitHub Actions does not prove whether a service is reachable from inside Iran. External probes, in-country observations, and browser-side checks are distinct measurement sources and should be interpreted separately.

## Live dashboard

Explore the current measurements, historical availability, latency, service groups, and available in-country observations:

<div align="center">

[**Open the IR Net Atlas dashboard →**](https://sinavm.github.io/ir-net-atlas/)

</div>

## Published data

The dashboard is backed by static JSON and SVG files published through GitHub Pages. They can also be consumed directly by scripts and other projects.

| Resource | Description |
|:--|:--|
| [Live status](https://sinavm.github.io/ir-net-atlas/status.json) | Latest external probe results, summary, and service-level measurements |
| [History](https://sinavm.github.io/ir-net-atlas/history.json) | Recent availability snapshots for timeline and trend analysis |
| [In-country observations](https://sinavm.github.io/ir-net-atlas/inside.json) | Latest available Radar or OONI-derived observations |
| [International targets](https://sinavm.github.io/ir-net-atlas/targets.json) | Curated targets used by browser-side checks |
| [Status badge](https://sinavm.github.io/ir-net-atlas/badge.svg) | Compact SVG summary for README files and other projects |

### Embed the status badge

Use the live badge in your own README:

```markdown
[![IR Net Atlas](https://sinavm.github.io/ir-net-atlas/badge.svg)](https://sinavm.github.io/ir-net-atlas/)
```

## How it works

1. **Collect targets** — the project loads its curated target definitions from the repository.
2. **Run external probes** — a scheduled GitHub Actions workflow checks the configured Iranian websites and APIs, recording HTTP status, response time, DNS timing, and a simple quality classification.
3. **Collect in-country observations** — a separate step queries public Radar data and falls back to OONI measurements when possible. If no fresh source is available, the last saved observation is retained and marked stale.
4. **Publish snapshots** — generated JSON, history, and badge files are committed to the repository and served by GitHub Pages.
5. **Explore the data** — the dashboard presents the available measurements and their timelines.

The workflow is scheduled to run hourly, with an additional run every three hours. Runs can also be started manually from [GitHub Actions](https://github.com/sinavm/ir-net-atlas/actions/workflows/probe.yml).

## Measurement details

Each external target may include:

- HTTP reachability and response status
- Request latency in milliseconds
- DNS resolution timing
- A coarse quality label: `fast`, `ok`, `slow`, or `down`
- A service group and measurement layer

Latency thresholds used by the current probe:

| Classification | Response time |
|:--|--:|
| Fast | Under 200 ms |
| OK | 200–799 ms |
| Slow | 800 ms or more |
| Down | Request failed or target was unreachable |

These labels are intentionally simple indicators, not service-level guarantees. A single request can be affected by transient routing, DNS, TLS, rate limiting, or server-side behavior.

## Repository layout

```text
.
├── .github/
│   └── workflows/
│       └── probe.yml          # Scheduled data collection workflow
├── docs/
│   ├── index.html              # GitHub Pages dashboard
│   ├── status.json             # Latest external probe snapshot
│   ├── history.json            # Recent historical snapshots
│   ├── inside.json             # In-country observations
│   ├── targets.json            # Browser-side target list
│   └── badge.svg               # Generated status badge
├── reports/
│   └── iran.json               # Local report data
├── fetch_inside.py             # Radar / OONI observation collector
├── observatory_targets.json    # External probe targets
├── targets.json                # International browser-side targets
└── probe.py                    # External reachability probe
```

## Run locally

Requirements: **Python 3.10+**. The collectors use the Python standard library and do not require third-party packages.

Run the external probe:

```bash
python3 probe.py
```

Fetch the latest available in-country observations:

```bash
python3 fetch_inside.py
```

The scripts write generated files to `docs/`. Running them locally does not publish the results; publication is handled by the GitHub Actions workflow.

## Contributing

Contributions that improve measurement quality, transparency, and data reliability are welcome.

- Add targets only when they are public, relevant, and reasonably stable.
- Keep external probes free of private credentials, personal data, and secret tokens.
- Preserve the distinction between measurements made outside Iran and observations collected inside Iran.
- Document the source and limitations of any new measurement.
- Avoid interpreting one failed request as proof of a nationwide outage.

For changes or questions, please open a [GitHub issue](https://github.com/sinavm/ir-net-atlas/issues) or submit a pull request.

## Disclaimer

IR Net Atlas is an independent measurement and research project. Results are snapshots from specific sources and vantage points; they may be incomplete, delayed, or affected by temporary network conditions. They should not be treated as a guarantee of availability or as a definitive measurement of every user's experience.

## License

This project is released under the [MIT License](LICENSE).

---

<div align="center">

**Built by [SiNAVM](https://github.com/sinavm)**

[Live Atlas](https://sinavm.github.io/ir-net-atlas/) · [Source code](https://github.com/sinavm/ir-net-atlas) · [Report an issue](https://github.com/sinavm/ir-net-atlas/issues)

</div>
