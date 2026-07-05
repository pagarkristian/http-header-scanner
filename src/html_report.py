import json

from src.constants import HEADER_INFORMATION, HEADER_WEIGHTS


STATUS_CLASS = {
    "Present": "present",
    "Missing": "missing",
    "Report Only": "report-only",
}

GRADE_BY_RISK = {
    "Low": "A",
    "Medium": "B",
    "High": "C",
    "Critical": "F",
}


def _percentage(part, total):
    """
    Calculate a rounded percentage, safely handling a zero total.
    """

    if total <= 0:
        return 0

    return round((part / total) * 100, 2)


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
                            <td class="header-name">{header}</td>
                            <td><span class="status-tag status-{status_class}">{info["status"]}</span></td>
                            <td class="header-value">{info["value"]}</td>
                        </tr>
"""

    return rows


def _build_recommendations(analysis):
    """
    Build recommendation list items for headers that are not fully present,
    ordered by their impact on the overall score (highest first).

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
        rows += f"""                <li class="rec-row">
                    <span class="rec-index">{index:02d}</span>
                    <div class="rec-body">
                        <div class="rec-heading">
                            <span class="rec-header-name">{header}</span>
                            <span class="rec-impact">impact {weight}</span>
                        </div>
                        <p class="rec-risk">{risk}</p>
                        <p class="rec-fix"><span class="rec-fix-label">Fix</span>{recommendation}</p>
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
        html = file.read()

    score = report["score"]
    risk_level = report["risk_level"]
    summary = report["summary"]
    total_headers = summary["present"] + summary["missing"] + summary["report_only"]

    html = html.replace(
        "{{TITLE}}",
        "HTTP Header Scanner Report",
    )

    html = html.replace(
        "{{SCANNER}}",
        report["scanner"],
    )

    html = html.replace(
        "{{VERSION}}",
        report["version"],
    )

    html = html.replace(
        "{{TIMESTAMP}}",
        report["timestamp"],
    )

    html = html.replace(
        "{{SCAN_DURATION}}",
        f'{report["scan_duration"]}s',
    )

    html = html.replace(
        "{{TARGET}}",
        report["target"],
    )

    html = html.replace(
        "{{FINAL_URL}}",
        report["final_url"],
    )

    html = html.replace(
        "{{STATUS_CODE}}",
        str(report["status_code"]),
    )

    html = html.replace(
        "{{SCORE}}",
        str(score),
    )

    html = html.replace(
        "{{SCORE_DEG}}",
        str(round(score * 3.6, 2)),
    )

    html = html.replace(
        "{{GRADE}}",
        GRADE_BY_RISK.get(risk_level, "F"),
    )

    html = html.replace(
        "{{RISK_LEVEL}}",
        risk_level,
    )

    html = html.replace(
        "{{RISK_LEVEL_CLASS}}",
        risk_level.lower(),
    )

    html = html.replace(
        "{{PRESENT}}",
        str(summary["present"]),
    )

    html = html.replace(
        "{{MISSING}}",
        str(summary["missing"]),
    )

    html = html.replace(
        "{{REPORT_ONLY}}",
        str(summary["report_only"]),
    )

    html = html.replace(
        "{{PRESENT_PCT}}",
        str(_percentage(summary["present"], total_headers)),
    )

    html = html.replace(
        "{{MISSING_PCT}}",
        str(_percentage(summary["missing"], total_headers)),
    )

    html = html.replace(
        "{{REPORT_ONLY_PCT}}",
        str(_percentage(summary["report_only"], total_headers)),
    )

    html = html.replace(
        "{{SUMMARY_NOTE}}",
        _build_summary_note(total_headers),
    )

    html = html.replace(
        "{{HEADER_TABLE}}",
        _build_header_table(report["analysis"]),
    )

    html = html.replace(
        "{{RECOMMENDATIONS}}",
        _build_recommendations(report["analysis"]),
    )

    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"HTML report saved to {html_file}")
