"""
Display functions for the HTTP Header Scanner.

This module owns all terminal presentation (built on Rich). It holds no
scanning, analysis, or scoring logic of its own — it only renders data
handed to it by main.py. The color palette intentionally mirrors the
HTML report so the CLI and the generated report read as the same product.
"""

from rich.align import Align
from rich.bar import Bar
from rich.box import DOUBLE, HEAVY, ROUNDED, SIMPLE_HEAVY
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from src.constants import HEADER_WEIGHTS


console = Console()

# ---------------------------------------------------------------------------
# Brand palette — kept in sync with the HTML report's color scheme.
# ---------------------------------------------------------------------------

BRAND = "#8B5CF6"
SUCCESS = "#35D399"
WARNING = "#F0B429"
HIGH = "#F0824A"
DANGER = "#F1476A"
MUTED = "grey62"
DIM_BORDER = "grey42"

RISK_COLOR = {
    "Low": SUCCESS,
    "Medium": WARNING,
    "High": HIGH,
    "Critical": DANGER,
}

GRADE_BY_RISK = {
    "Low": "A",
    "Medium": "B",
    "High": "C",
    "Critical": "F",
}

STATUS_STYLE = {
    "Present": (SUCCESS, "\u2713"),
    "Report Only": (WARNING, "\u25B2"),
    "Missing": (DANGER, "\u2717"),
}


def _severity_from_weight(weight):
    """
    Map a header's scoring weight to the same severity vocabulary and
    color scale used for the overall risk level, so "severity" means the
    same thing everywhere in the tool.

    Args:
        weight (int): The header's weight from HEADER_WEIGHTS.

    Returns:
        tuple[str, str]: (label, color)
    """

    if weight >= 30:
        return "CRITICAL", DANGER

    if weight >= 20:
        return "HIGH", HIGH

    if weight >= 12:
        return "MEDIUM", WARNING

    return "LOW", SUCCESS


# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

def display_banner():
    """
    Display the application banner.
    """

    title = Text("HTTP HEADER SCANNER", style=f"bold {BRAND}")
    subtitle = Text("Website Security Header Audit Tool", style=MUTED)
    body = Text()
    body.append_text(title)
    body.append("\n")
    body.append_text(subtitle)

    console.print()
    console.print(
        Panel(
            Align.center(body),
            border_style=BRAND,
            box=HEAVY,
            padding=(1, 4),
        )
    )


# ---------------------------------------------------------------------------
# Scan lifecycle
# ---------------------------------------------------------------------------

def scanning_status(url):
    """
    Return a Rich status context manager that shows a spinner while the
    target is being scanned. Any output printed by the scanning engine
    during this time (e.g. a connection error) is safely displayed above
    the spinner by Rich's live-display stdout redirection.

    Args:
        url (str): Target URL.

    Returns:
        rich.console.Status: Use with a `with` statement.
    """

    message = Text()
    message.append("Scanning ", style=f"bold {BRAND}")
    message.append(url, style="white")

    return console.status(message, spinner="dots")


def saving_status():
    """
    Return a Rich status context manager shown while reports are written
    to disk.

    Returns:
        rich.console.Status: Use with a `with` statement.
    """

    return console.status(
        f"[bold {BRAND}]Saving reports...[/]",
        spinner="dots",
    )


def display_scan_success(response):
    """
    Display a success panel after a completed scan.

    Args:
        response (requests.Response): HTTP response.
    """

    body = Text()
    body.append("Final URL    ", style=MUTED)
    body.append(f"{response.url}\n")
    body.append("Status Code  ", style=MUTED)
    body.append(f"{response.status_code}", style=f"bold {SUCCESS}")

    console.print()
    console.print(
        Panel(
            body,
            title="[bold]Request Completed[/]",
            title_align="left",
            border_style=SUCCESS,
            box=ROUNDED,
            padding=(1, 2),
        )
    )


def display_scan_error(url):
    """
    Display an error panel when a scan could not be completed.

    Args:
        url (str): Target URL that failed to respond.
    """

    message = Text()
    message.append("Could not complete the scan for ")
    message.append(url, style="bold")
    message.append(".\n")
    message.append("See the error above for details.", style=MUTED)

    console.print()
    console.print(
        Panel(
            message,
            title="[bold]Scan Failed[/]",
            title_align="left",
            border_style=DANGER,
            box=ROUNDED,
            padding=(1, 2),
        )
    )


# ---------------------------------------------------------------------------
# Response headers
# ---------------------------------------------------------------------------

def display_headers(headers):
    """
    Display all HTTP response headers.

    Args:
        headers (dict): HTTP response headers.
    """

    table = Table(
        title="Response Headers",
        title_style=f"bold {BRAND}",
        title_justify="left",
        box=SIMPLE_HEAVY,
        border_style=DIM_BORDER,
        header_style=f"bold {BRAND}",
        padding=(0, 1),
        expand=True,
    )

    table.add_column("Header", style="bold white", ratio=2, no_wrap=True)
    table.add_column("Value", style=MUTED, ratio=5, overflow="fold")

    for key, value in headers.items():
        table.add_row(Text(key), Text(str(value)))

    console.print()
    console.print(table)


# ---------------------------------------------------------------------------
# Security analysis
# ---------------------------------------------------------------------------

def run_with_progress(description, func, *args, **kwargs):
    """
    Run a single function call behind a short-lived Rich progress bar.

    This is purely a visual wrapper around an existing call — it does not
    alter what is computed or the order calls happen in, only how the
    (usually brief) wait is presented.

    Args:
        description (str): Label shown next to the progress bar.
        func (callable): Function to call.
        *args: Positional arguments passed to func.
        **kwargs: Keyword arguments passed to func.

    Returns:
        The return value of func(*args, **kwargs).
    """

    with Progress(
        SpinnerColumn(style=BRAND),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30, complete_style=BRAND, finished_style=SUCCESS),
        TextColumn("[{task.percentage:>3.0f}%]", markup=False),
        console=console,
        transient=True,
    ) as progress:

        task = progress.add_task(description, total=1)
        result = func(*args, **kwargs)
        progress.update(task, completed=1)

    return result


def display_security_analysis(analysis):
    """
    Display the security header analysis.

    Args:
        analysis (dict): Security analysis results.
    """

    table = Table(
        title="Security Header Analysis",
        title_style=f"bold {BRAND}",
        title_justify="left",
        box=SIMPLE_HEAVY,
        border_style=DIM_BORDER,
        header_style=f"bold {BRAND}",
        padding=(0, 1),
        expand=True,
    )

    table.add_column("", width=2, justify="center")
    table.add_column("Header", style="bold white", ratio=2, no_wrap=True)
    table.add_column("Status", ratio=2)
    table.add_column("Value", style=MUTED, ratio=4, overflow="fold")

    for header, info in analysis.items():
        color, symbol = STATUS_STYLE.get(info["status"], (DANGER, "?"))

        table.add_row(
            Text(symbol, style=f"bold {color}"),
            Text(header),
            Text(info["status"], style=f"bold {color}"),
            Text(str(info["value"]), style=MUTED if info["value"] != "N/A" else "grey42"),
        )

    console.print()
    console.print(table)


# ---------------------------------------------------------------------------
# Security score
# ---------------------------------------------------------------------------

def display_security_score(score, risk_level):
    """
    Display the security score.

    Args:
        score (int): Security score.
        risk_level (str): Risk level.
    """

    color = RISK_COLOR.get(risk_level, DANGER)
    grade = GRADE_BY_RISK.get(risk_level, "F")

    headline = Text()
    headline.append(f" {grade} ", style=f"bold black on {color}")
    headline.append(f"  {score}", style=f"bold {color}")
    headline.append("/100    ", style=MUTED)
    headline.append(f"{risk_level.upper()} RISK", style=f"bold {color}")

    bar = Bar(size=100, begin=0, end=score, color=color, bgcolor="grey19")

    content = Table.grid(padding=(1, 0, 0, 0))
    content.add_column()
    content.add_row(headline)
    content.add_row(bar)

    console.print()
    console.print(
        Panel(
            content,
            title="[bold]Security Score[/]",
            title_align="left",
            border_style=color,
            box=ROUNDED,
            padding=(1, 2),
        )
    )


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

def display_security_recommendations(analysis, header_information):
    """
    Display security recommendations, ordered by their impact on the
    overall score (highest first).

    Args:
        analysis (dict): Security analysis results.
        header_information (dict): Security header information.
    """

    items = []

    for header, info in analysis.items():

        if info["present"]:
            continue

        details = header_information[header]
        weight = HEADER_WEIGHTS.get(header, 0)

        if info["status"] == "Report Only":
            recommendation = "Deploy an enforced Content-Security-Policy header."
        else:
            recommendation = details["recommendation"]

        items.append((weight, header, details["risk"], recommendation))

    console.print()

    if not items:
        console.print(
            Panel(
                "No issues found. All security headers are properly configured.",
                title="[bold]Recommendations[/]",
                title_align="left",
                border_style=SUCCESS,
                box=ROUNDED,
                padding=(1, 2),
            )
        )
        return

    items.sort(key=lambda item: item[0], reverse=True)

    table = Table(
        title="Recommendations",
        title_style=f"bold {BRAND}",
        title_justify="left",
        caption="ordered by impact on score",
        caption_style=MUTED,
        caption_justify="left",
        box=SIMPLE_HEAVY,
        border_style=DIM_BORDER,
        header_style=f"bold {BRAND}",
        padding=(0, 1),
        expand=True,
        show_lines=True,
    )

    table.add_column("#", width=3, justify="right", style=MUTED)
    table.add_column("Severity", width=10)
    table.add_column("Header", ratio=2, no_wrap=True)
    table.add_column("Risk / Recommendation", ratio=5)

    for index, (weight, header, risk, recommendation) in enumerate(items, start=1):
        severity_label, severity_color = _severity_from_weight(weight)

        detail = Text()
        detail.append("Risk  ", style=f"bold {MUTED}")
        detail.append(f"{risk}\n")
        detail.append("Fix   ", style=f"bold {MUTED}")
        detail.append(recommendation)

        table.add_row(
            str(index),
            Text(f" {severity_label} ", style=f"bold black on {severity_color}"),
            Text(header),
            detail,
        )

    console.print(table)


# ---------------------------------------------------------------------------
# Closing summary
# ---------------------------------------------------------------------------

def display_scan_summary(url, response, score, risk_level, scan_duration, json_path, html_path):
    """
    Display a closing summary panel once both reports have been written.

    Args:
        url (str): Original target URL.
        response (requests.Response): HTTP response.
        score (int): Security score.
        risk_level (str): Risk level.
        scan_duration (float): Scan duration in seconds.
        json_path (str): Path to the written JSON report.
        html_path (str): Path to the written HTML report.
    """

    color = RISK_COLOR.get(risk_level, DANGER)

    grid = Table.grid(padding=(0, 2))
    grid.add_column(style=MUTED, no_wrap=True)
    grid.add_column()

    grid.add_row("Target", Text(url))
    grid.add_row("Final URL", Text(response.url))
    grid.add_row("Score", f"[bold {color}]{score}/100[/]")
    grid.add_row("Risk Level", f"[bold {color}]{risk_level}[/]")
    grid.add_row("Duration", f"{scan_duration}s")
    grid.add_row("JSON Report", str(json_path))
    grid.add_row("HTML Report", str(html_path))

    console.print()
    console.print(
        Panel(
            grid,
            title="[bold]Scan Summary[/]",
            title_align="left",
            subtitle="[dim]Run complete[/]",
            subtitle_align="right",
            border_style=BRAND,
            box=DOUBLE,
            padding=(1, 2),
        )
    )
    console.print()
