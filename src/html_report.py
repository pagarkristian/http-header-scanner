import json


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
        f'{report["scan_duration"]} seconds',
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
        f'{report["score"]}/100',
    )

    html = html.replace(
        "{{RISK_LEVEL}}",
        report["risk_level"],
    )

    html = html.replace(
        "{{PRESENT}}",
        str(report["summary"]["present"]),
    )

    html = html.replace(
        "{{MISSING}}",
        str(report["summary"]["missing"]),
    )

    html = html.replace(
        "{{REPORT_ONLY}}",
        str(report["summary"]["report_only"]),
    )

    table = """
<h2>Security Header Analysis</h2>

<table>

<tr>

<th>Header</th>

<th>Status</th>

<th>Value</th>

</tr>
"""

    for header, info in report["analysis"].items():

        table += f"""
<tr>

<td>{header}</td>

<td>{info["status"]}</td>

<td>{info["value"]}</td>

</tr>
"""

    table += """
</table>
"""

    html = html.replace(
        "{{HEADER_TABLE}}",
        table,
    )

    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"HTML report saved to {html_file}")
