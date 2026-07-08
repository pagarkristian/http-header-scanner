# HTTP Header Scanner

A Python CLI tool that scans a website's HTTP response, checks it against a set of
modern security headers and cookie security attributes, and produces a security
score, a professional CLI report, and a downloadable HTML/JSON report.

Built as a learning project to practice Python and core web application security
concepts (security headers, cookie flags, cross-origin isolation) while producing a
tool that works like real-world scanners such as Mozilla Observatory or
SecurityHeaders.com.

---

## Features

- **HTTP Header Scanning** — fetches a target URL and reads all response headers.
- **Security Header Analysis** — checks 10 modern security headers, including
  Content-Security-Policy, Strict-Transport-Security, and cross-origin isolation
  headers (COOP / COEP / CORP).
- **Cookie Security Analysis** — checks every `Set-Cookie` header for `Secure`,
  `HttpOnly`, `SameSite`, and expiry.
- **Security Score & Risk Level** — a weighted 0–100 score with a Low/Medium/High/
  Critical risk level.
- **Professional CLI Output** — built with [Rich](https://github.com/Textualize/rich):
  tables, progress bars, and colored panels.
- **HTML & JSON Reports** — a shareable, styled HTML report and a machine-readable
  JSON report saved per scan.
- **Batch Scanning** — scan a list of URLs from a text file with `--file`.
- **Per-Domain Reports** — each target gets its own `reports/<domain>/` folder.
- **Configurable via `config.ini`** — timeout, output folder, and logging are all
  configurable without touching code.
- **Logging** — every scan is recorded to `logs/scanner.log` for later review.
- **Graceful Error Handling** — connection failures and unexpected errors show a
  clean message instead of crashing the whole batch.

---

## Installation

```bash
git clone https://github.com/<your-username>/http-header-scanner.git
cd http-header-scanner
pip install -r requirements.txt
```

Requires Python 3.9+.

---

## Usage

### Scan a single target

```bash
python -m src.main https://example.com
```

You can also run it without an argument and it will prompt for a URL:

```bash
python -m src.main
```

### Scan multiple targets from a file

```bash
python -m src.main --file examples/multi_targets.txt
```

See `examples/single_target.txt` and `examples/multi_targets.txt` for the expected
file format (one URL per line, `#` for comments).

### Check the version

```bash
python -m src.main --version
```

Each scan produces:
```
reports/<domain>/report.json
reports/<domain>/report.html
```

A sample report is available at `examples/sample_report.json`.

---

## Configuration

On first run, a `config.ini` file is created automatically with these defaults:

```ini
[scanner]
timeout = 10

[output]
reports_dir = reports

[logging]
logs_dir = logs
log_level = INFO
```

Edit `config.ini` to change the request timeout, where reports are saved, or the
logging verbosity — no code changes needed.

---

## Project Structure

```
http-header-scanner/
├── src/
│   ├── main.py             # CLI entry point / scan orchestration
│   ├── scanner.py          # HTTP requests
│   ├── analyzer.py         # Security header analysis
│   ├── cookie_analyzer.py  # Cookie security analysis
│   ├── scoring.py          # Security score & risk level calculation
│   ├── constants.py        # Header list, weights, and risk/recommendation text
│   ├── display.py          # Rich CLI output
│   ├── exporter.py         # JSON report writer
│   ├── html_report.py      # HTML report generator
│   ├── config.py           # config.ini loader
│   ├── logger_config.py    # Logging setup
│   └── utils.py            # File/target loading helpers
├── templates/report.html   # HTML report template
├── static/style.css        # HTML report styling
├── examples/                # Example target files and a sample report
├── docs/                    # Architecture notes and per-version dev notes
├── tests/                   # Unit tests
└── config.ini                # Auto-generated on first run
```

See `docs/architecture.md` for how data flows between these modules.

---

## Security Headers Checked

| Header | Purpose |
|---|---|
| Content-Security-Policy | Restricts which sources scripts/styles/etc. can load from |
| Strict-Transport-Security | Forces HTTPS for future visits |
| X-Frame-Options | Prevents the page from being framed (clickjacking) |
| X-Content-Type-Options | Stops MIME-type sniffing |
| Referrer-Policy | Controls what referrer info is sent to other sites |
| Permissions-Policy | Restricts browser features (camera, geolocation, etc.) |
| Cross-Origin-Opener-Policy | Isolates the page's window from other origins |
| Cross-Origin-Embedder-Policy | Requires explicit opt-in for cross-origin resources |
| Cross-Origin-Resource-Policy | Restricts who can load this site's resources |
| X-Permitted-Cross-Domain-Policies | Restricts legacy plugin cross-domain access |

## Cookie Attributes Checked

`Secure`, `HttpOnly`, `SameSite`, and expiry (`Expires` / `Max-Age`).

---

## Version History

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for planned future improvements.

## License

See [LICENSE](LICENSE).
