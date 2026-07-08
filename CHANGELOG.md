# Changelog

All notable changes to this project are documented in this file.

## [3.8] - Release Candidate
### Changed
- Reviewed the whole project for consistent naming, imports, and formatting.
- Synced version numbers across `--version`, JSON report output, and docs.
- Filled in `pyproject.toml` with project metadata.

## [3.7] - Project Polish
### Added
- Full `README.md` (features, installation, usage, configuration, project structure).
- `docs/architecture.md` describing module responsibilities and data flow.
- `docs/roadmap.md` describing completed milestones and future ideas.
- Populated `examples/single_target.txt` and `examples/sample_report.json`.
### Changed
- Reviewed docstrings and comments across all modules for clarity.

## [3.6] - Application Improvements
### Added
- `src/config.py` — `config.ini`-based application configuration (timeout, output
  folder, logging), auto-created with defaults on first run.
- `src/logger_config.py` — file-based logging to `logs/scanner.log`.
- `display_unexpected_error()` — clean error panel for unexpected exceptions.
### Changed
- `scanner.scan_website()` now accepts a configurable `timeout` and auto-adds a
  scheme (`https://`) if the user forgets one.
- `utils.create_report_directory()` now accepts a configurable `reports_dir`.
- `main.scan_target()` wraps the full scan flow in error handling so one failing
  target can't crash an entire batch scan.

## [3.5] - Cookie Security Analysis
### Added
- `src/cookie_analyzer.py` — analyzes `Set-Cookie` headers for `Secure`,
  `HttpOnly`, `SameSite`, and expiry.
- Cookie Security Analysis section in the CLI output and HTML report.
- `cookies` and `cookie_summary` fields in the JSON report.

## [3.4] - Advanced Security Headers
### Added
- Four new security headers: `Cross-Origin-Opener-Policy`,
  `Cross-Origin-Embedder-Policy`, `Cross-Origin-Resource-Policy`, and
  `X-Permitted-Cross-Domain-Policies`.
### Changed
- Rebalanced `HEADER_WEIGHTS` across all 10 headers so the total still sums to 100.

## [3.0 - 3.3]
### Added
- Initial working version: HTTP scanning, security header analysis, security
  scoring and risk level, professional Rich-based CLI, HTML and JSON report
  generation, progress spinners, command-line argument parsing, single and batch
  (`--file`) scanning, per-domain report folders.
