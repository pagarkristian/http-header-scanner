import json
from datetime import datetime


def export_to_json(
    filename,
    target,
    response,
    analysis,
    score,
    risk_level,
    scan_duration,
):
    """
    Export scan results to a JSON file.

    Args:
        filename (str): Output filename.
        target (str): Target URL.
        response (requests.Response): HTTP response.
        analysis (dict): Security analysis results.
        score (int): Security score.
        risk_level (str): Overall risk level.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    present_count = 0
    missing_count = 0
    report_only_count = 0

    for info in analysis.values():

        if info["status"] == "Present":
            present_count += 1

        elif info["status"] == "Missing":
            missing_count += 1

        elif info["status"] == "Report Only":
            report_only_count += 1

    report = {
        "scanner": "HTTP Header Scanner",
        "version": "1.10",
        "timestamp": timestamp,
        "scan_duration": scan_duration,
        "target": target,
        "final_url": response.url,
        "status_code": response.status_code,
        "score": score,
        "risk_level": risk_level,

        "summary": {
            "present": present_count,
            "missing": missing_count,
            "report_only": report_only_count,
        },

        "analysis": analysis,
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"\nReport saved to: {filename}")
