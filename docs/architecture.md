# Architecture

## Design Philosophy

This project is intentionally kept simple: plain functions grouped by
responsibility, no classes unless a module genuinely needs to hold state, and one
config-driven source of truth (`constants.py`) for anything data-like (header list,
weights, risk descriptions) so that adding a new header or cookie check doesn't
require touching logic code.

## Modules

| Module | Responsibility |
|---|---|
| `main.py` | Parses CLI args, orchestrates a scan end-to-end, wires config + logger + error handling together. |
| `scanner.py` | Sends the HTTP GET request. Only knows about `requests`. |
| `analyzer.py` | Compares response headers against `SECURITY_HEADERS` and classifies each as Present / Missing / Report Only. |
| `cookie_analyzer.py` | Parses `Set-Cookie` headers and checks security attributes. |
| `scoring.py` | Sums `HEADER_WEIGHTS` for present headers into a 0–100 score and risk level. |
| `constants.py` | Single source of truth: which headers are checked, their scoring weight, and their risk/recommendation text. |
| `config.py` | Loads (and auto-creates) `config.ini` for timeout, output folder, and logging settings. |
| `logger_config.py` | Sets up the shared file logger. |
| `display.py` | All Rich-based terminal output. Holds no logic — only renders data it's given. |
| `exporter.py` | Writes the JSON report. |
| `html_report.py` | Fills `templates/report.html` with data from the JSON report. |
| `utils.py` | Small file-system helpers (loading target lists, creating report folders). |

## Data Flow

```
                 ┌─────────────┐
   CLI args ---> │   main.py   │
                 └──────┬──────┘
                        │
                        v
                 ┌─────────────┐
                 │ scanner.py  │  -->  requests.get(url)
                 └──────┬──────┘
                        │ response
          ┌─────────────┼──────────────┐
          v                            v
   ┌──────────────┐            ┌─────────────────┐
   │ analyzer.py   │            │ cookie_analyzer  │
   └──────┬────────┘            └────────┬─────────┘
          │ analysis                     │ cookies
          v                              │
   ┌──────────────┐                      │
   │  scoring.py   │                     │
   └──────┬────────┘                     │
          │ score, risk_level            │
          └───────────────┬──────────────┘
                           v
                  ┌─────────────────┐
                  │    display.py    │  -->  CLI output (Rich)
                  ├─────────────────┤
                  │   exporter.py    │  -->  reports/<domain>/report.json
                  ├─────────────────┤
                  │  html_report.py  │  -->  reports/<domain>/report.html
                  └─────────────────┘
```

## Why headers and weights live in `constants.py`

`analyzer.py`, `scoring.py`, and `display.py` never hardcode a header name — they
all loop over `SECURITY_HEADERS` / `HEADER_WEIGHTS`. This means adding a new header
only requires editing `constants.py` (see `docs/v3.4_notes.md` for a concrete
example). The same principle keeps `HEADER_WEIGHTS` summing to 100: the score is
always "how many of the possible 100 points did this site earn."

## Why `Set-Cookie` is read from `response.raw`

`requests` normally collapses repeated headers into a single comma-joined string.
`Set-Cookie` is a special case: a server can send several `Set-Cookie` headers, and
their values (like `Expires` dates) can themselves contain commas, so naive joining
corrupts the data. `cookie_analyzer.py` reads
`response.raw.headers.getlist("Set-Cookie")` instead, which keeps each header
separate. See `docs/v3.5_notes.md` for details.
