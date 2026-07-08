# Roadmap

## Completed (v3.0 - v3.8)

- [x] Core HTTP scanning, header analysis, scoring, and risk level (v3.0 - v3.3)
- [x] Professional Rich-based CLI and HTML/JSON reports (v3.0 - v3.3)
- [x] Batch scanning and per-domain reports (v3.0 - v3.3)
- [x] Advanced/cross-origin isolation security headers (v3.4)
- [x] Cookie security analysis (v3.5)
- [x] Logging, configuration file, and better error handling (v3.6)
- [x] Documentation, examples, and project polish (v3.7)
- [x] Release candidate review (v3.8)

## Ideas for a Future v4

These are intentionally *not* implemented yet, to keep the v3 scope focused and
achievable. Listed here so the project has a clear next direction.

- **Concurrent batch scanning** — scan multiple targets in parallel (e.g. with
  `concurrent.futures` or `asyncio` + `aiohttp`) instead of sequentially.
- **CSP policy quality checks** — not just "is CSP present," but flag weak
  directives like `unsafe-inline` or a wildcard `*` source.
- **Historical comparison** — compare a new scan against the previous scan for the
  same domain and highlight what changed.
- **CI-friendly output mode** — a `--fail-below <score>` flag that exits non-zero,
  so the scanner can be used as a CI/CD security gate.
- **Config via environment variables** — allow overriding `config.ini` values with
  env vars for containerized/CI environments.
- **Unit test coverage** — the `tests/` folder currently contains empty
  placeholders; a real test suite (especially for `analyzer.py`, `scoring.py`, and
  `cookie_analyzer.py`, which have no external dependencies) would be a strong
  addition for the portfolio.
