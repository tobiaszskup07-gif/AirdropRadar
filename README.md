# AirdropRadar

Open-source dashboard for source-backed crypto airdrop announcements across Solana, Ethereum and Base.

## Quick start

Requires Python 3.10+. Run `python -m src.app` and visit http://localhost:8000. JSON API: `/api/announcements`. The dashboard also supports static hosting on GitHub Pages.

## Tests

Run `python -m unittest discover -s tests -v`.

## Data and contributions

Add verified announcements to `data/announcements.json` using string fields `project`, `chain`, `status`, `source_url`, and `summary`. Link to primary sources and distinguish confirmed claims from speculation. The initial feed is empty. Open an issue or pull request to contribute.

## Roadmap

- Dashboard and chain filters (implemented)
- JSON API (implemented)
- Official source ingestion, deduplication and deadline alerts (planned)

No wallet connection or signing. Never share seed phrases. Not financial advice.

MIT license.
