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
    cookies,
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
        scan_duration (float): Scan duration in seconds.
        cookies (list[dict]): Cookie analysis results from
            cookie_analyzer.analyze_cookies().
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

    cookies_secure_count = sum(1 for cookie in cookies if cookie["status"] == "Secure")
    cookies_needs_attention_count = len(cookies) - cookies_secure_count

    report = {
        "scanner": "HTTP Header Scanner",
        "version": "3.8",
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

        "cookies": cookies,
        "cookie_summary": {
            "total": len(cookies),
            "secure": cookies_secure_count,
            "needs_attention": cookies_needs_attention_count,
        },
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"\nReport saved to: {filename}")
