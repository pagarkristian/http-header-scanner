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

    html = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>HTTP Header Scanner Report</title>
</head>

<body>

    <h1>HTTP Header Scanner Report</h1>

    <hr>

    <h2>General Information</h2>

    <p><strong>Scanner:</strong> {report["scanner"]}</p>

    <p><strong>Version:</strong> {report["version"]}</p>

    <p><strong>Timestamp:</strong> {report["timestamp"]}</p>

    <p><strong>Scan Duration:</strong> {report["scan_duration"]} seconds</p>

    <hr>

    <h2>Target</h2>

    <p><strong>URL:</strong> {report["target"]}</p>

    <p><strong>Final URL:</strong> {report["final_url"]}</p>

    <p><strong>Status Code:</strong> {report["status_code"]}</p>

    <hr>

    <h2>Security Result</h2>

    <p><strong>Score:</strong> {report["score"]}/100</p>

    <p><strong>Risk Level:</strong> {report["risk_level"]}</p>

    <hr>

    <h2>Summary</h2>

    <ul>
        <li>Present : {report["summary"]["present"]}</li>
        <li>Missing : {report["summary"]["missing"]}</li>
        <li>Report Only : {report["summary"]["report_only"]}</li>
    </ul>

</body>

</html>
"""

    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"HTML report saved to: {html_file}")
