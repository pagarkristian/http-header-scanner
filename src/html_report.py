import html
import json

from src.constants import HEADER_INFORMATION, HEADER_WEIGHTS


STATUS_CLASS = {
    "Present": "present",
    "Missing": "missing",
    "Report Only": "report-only",
}

COOKIE_STATUS_CLASS = {
    "Secure": "present",
    "Needs Attention": "missing",
}

GRADE_BY_RISK = {
    "Low": "A",
    "Medium": "B",
    "High": "C",
    "Critical": "F",
}

# Long header values (e.g. Content-Security-Policy) are collapsed behind a
# native <details> toggle so the table keeps a consistent row height.
VALUE_TRUNCATE_LENGTH = 64


def _esc(value):
    """
    HTML-escape a value pulled from the JSON report before it is dropped
    into the template. Header values come straight from a remote server,
    so they are treated as untrusted input.
    """

    return html.escape(str(value), quote=True)


def _percentage(part, total):
    """
    Calculate a rounded percentage, safely handling a zero total.
    """

    if total <= 0:
        return 0

    return round((part / total) * 100, 2)


def _severity_from_weight(weight):
    """
    Map a header's scoring weight to the same severity vocabulary and
    color scale already used for the overall Risk Level, so severity
    means the same thing everywhere in the report.

    Args:
        weight (int): The header's weight from HEADER_WEIGHTS.

    Returns:
        tuple[str, str]: (label, css_class)
    """

    if weight >= 30:
        return "Critical", "critical"

    if weight >= 20:
        return "High", "high"

    if weight >= 12:
        return "Medium", "medium"

    return "Low", "low"


def _build_summary_note(total_headers):
    """
    Build an optional note shown when there is no header data to summarize.

    Args:
        total_headers (int): Total number of headers evaluated.

    Returns:
        str: HTML note, or an empty string when not needed.
    """

    if total_headers == 0:
        return '<p class="summary-empty-note">No security headers were detected in the response.</p>'

    return ""


def _render_value_cell(value):
    """
    Render a header value cell. Short values are shown as-is; long values
    (e.g. Content-Security-Policy) are truncated to a single line with a
    native, keyboard-accessible <details> toggle to reveal the full value.
    This keeps every table row the same height regardless of content.

    Args:
        value (str): Raw header value.

    Returns:
        str: HTML for the table cell contents.
    """

    safe_value = _esc(value)

    if len(value) <= VALUE_TRUNCATE_LENGTH:
        return f'<span class="value-text">{safe_value}</span>'

    preview = _esc(value[:VALUE_TRUNCATE_LENGTH].rstrip()) + "&hellip;"

    return f"""<details class="value-details">
                                <summary class="value-summary" title="{safe_value}">
                                    <span class="value-text">{preview}</span>
                                    <span class="value-toggle">Show full value</span>
                                </summary>
                                <div class="value-full">{safe_value}</div>
                            </details>"""


def _build_header_table(analysis):
    """
    Build the security header analysis table rows.

    Args:
        analysis (dict): Security analysis results.

    Returns:
        str: HTML table rows.
    """

    if not analysis:
        return (
            '                        <tr class="row-empty">'
            '<td colspan="3" class="table-empty">'
            "No headers were captured for this response."
            "</td></tr>\n"
        )

    rows = ""

    for header, info in analysis.items():
        status_class = STATUS_CLASS.get(info["status"], "missing")

        rows += f"""                        <tr class="row-{status_class}">
                            <td class="header-name">{_esc(header)}</td>
                            <td><span class="status-tag status-{status_class}">{_esc(info["status"])}</span></td>
                            <td class="header-value">{_render_value_cell(info["value"])}</td>
                        </tr>
"""

    return rows


def _build_cookie_table(cookies):
    """
    Build the cookie security analysis table rows.

    Args:
        cookies (list[dict]): Cookie analysis results from
            cookie_analyzer.analyze_cookies().

    Returns:
        str: HTML table rows.
    """

    if not cookies:
        return (
            '                        <tr class="row-empty">'
            '<td colspan="5" class="table-empty">'
            "This response did not set any cookies."
            "</td></tr>\n"
        )

    rows = ""

    for cookie in cookies:
        status_class = COOKIE_STATUS_CLASS.get(cookie["status"], "missing")
        issues = "; ".join(cookie["issues"]) if cookie["issues"] else "None"

        rows += f"""                        <tr class="row-{status_class}">
                            <td class="header-name">{_esc(cookie["name"])}</td>
                            <td><span class="status-tag status-{status_class}">{_esc(cookie["status"])}</span></td>
                            <td>{"Yes" if cookie["secure"] else "No"}</td>
                            <td>{"Yes" if cookie["httponly"] else "No"}</td>
                            <td class="header-value">{_esc(cookie["samesite"] or "Not set")} &mdash; {_esc(issues)}</td>
                        </tr>
"""

    return rows


def _build_recommendations(analysis):
    """
    Build recommendation list items for headers that are not fully present,
    ordered by their impact on the overall score (highest first). Each item
    surfaces severity, header name, risk description, fix, priority, and
    impact score.

    Args:
        analysis (dict): Security analysis results.

    Returns:
        str: HTML <li> rows.
    """

    if not analysis:
        return (
            '                <li class="rec-empty">'
            "No headers were captured, so no recommendations could be generated."
            "</li>\n"
        )

    items = []

    for header, info in analysis.items():

        if info["present"]:
            continue

        details = HEADER_INFORMATION.get(header)

        if not details:
            continue

        if info["status"] == "Report Only":
            recommendation = "Deploy an enforced Content-Security-Policy header."
        else:
            recommendation = details["recommendation"]

        weight = HEADER_WEIGHTS.get(header, 0)

        items.append((weight, header, details["risk"], recommendation))

    items.sort(key=lambda item: item[0], reverse=True)

    rows = ""

    for index, (weight, header, risk, recommendation) in enumerate(items, start=1):
        severity_label, severity_class = _severity_from_weight(weight)

        rows += f"""                <li class="rec-row">
                    <div class="rec-priority">
                        <span class="rec-index">{index:02d}</span>
                        <span class="rec-priority-label">Priority</span>
                    </div>
                    <div class="rec-body">
                        <div class="rec-heading">
                            <span class="badge-pill risk-{severity_class}"><span class="badge-dot"></span>{severity_label}</span>
                            <span class="rec-header-name">{_esc(header)}</span>
                            <span class="rec-impact">+{weight} pts impact</span>
                        </div>
                        <p class="rec-risk"><span class="rec-label">Risk</span>{_esc(risk)}</p>
                        <p class="rec-fix"><span class="rec-label">Fix</span>{_esc(recommendation)}</p>
                    </div>
                </li>
"""

    if not rows:
        rows = '                <li class="rec-empty">No issues found. All security headers are properly configured.</li>\n'

    return rows


def generate_html_report(json_file, html_file):
    """
    Generate an HTML report from a JSON report.

    Args:
        json_file (str): Input JSON report.
        html_file (str): Output HTML report.
    """

    with open(json_file, "r", encoding="utf-8") as file:
        report = json.load(file)

    with open("templates/report.html", "r", encoding="utf-8") as file:
        html_out = file.read()

    score = report["score"]
    risk_level = report["risk_level"]
    summary = report["summary"]
    total_headers = summary["present"] + summary["missing"] + summary["report_only"]

    html_out = html_out.replace(
        "{{TITLE}}",
        "HTTP Header Scanner Report",
    )

    html_out = html_out.replace(
        "{{SCANNER}}",
        _esc(report["scanner"]),
    )

    html_out = html_out.replace(
        "{{VERSION}}",
        _esc(report["version"]),
    )

    html_out = html_out.replace(
        "{{TIMESTAMP}}",
        _esc(report["timestamp"]),
    )

    html_out = html_out.replace(
        "{{SCAN_DURATION}}",
        f'{report["scan_duration"]}s',
    )

    html_out = html_out.replace(
        "{{TARGET}}",
        _esc(report["target"]),
    )

    html_out = html_out.replace(
        "{{FINAL_URL}}",
        _esc(report["final_url"]),
    )

    html_out = html_out.replace(
        "{{STATUS_CODE}}",
        str(report["status_code"]),
    )

    html_out = html_out.replace(
        "{{SCORE}}",
        str(score),
    )

    html_out = html_out.replace(
        "{{SCORE_DEG}}",
        str(round(score * 3.6, 2)),
    )

    html_out = html_out.replace(
        "{{GRADE}}",
        GRADE_BY_RISK.get(risk_level, "F"),
    )

    html_out = html_out.replace(
        "{{RISK_LEVEL}}",
        _esc(risk_level),
    )

    html_out = html_out.replace(
        "{{RISK_LEVEL_CLASS}}",
        risk_level.lower(),
    )

    html_out = html_out.replace(
        "{{PRESENT}}",
        str(summary["present"]),
    )

    html_out = html_out.replace(
        "{{MISSING}}",
        str(summary["missing"]),
    )

    html_out = html_out.replace(
        "{{REPORT_ONLY}}",
        str(summary["report_only"]),
    )

    html_out = html_out.replace(
        "{{PRESENT_PCT}}",
        str(_percentage(summary["present"], total_headers)),
    )

    html_out = html_out.replace(
        "{{MISSING_PCT}}",
        str(_percentage(summary["missing"], total_headers)),
    )

    html_out = html_out.replace(
        "{{REPORT_ONLY_PCT}}",
        str(_percentage(summary["report_only"], total_headers)),
    )

    html_out = html_out.replace(
        "{{SUMMARY_NOTE}}",
        _build_summary_note(total_headers),
    )

    html_out = html_out.replace(
        "{{HEADER_TABLE}}",
        _build_header_table(report["analysis"]),
    )

    html_out = html_out.replace(
        "{{COOKIE_TABLE}}",
        _build_cookie_table(report.get("cookies", [])),
    )

    html_out = html_out.replace(
        "{{RECOMMENDATIONS}}",
        _build_recommendations(report["analysis"]),
    )

    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html_out)

    print(f"HTML report saved to {html_file}")
