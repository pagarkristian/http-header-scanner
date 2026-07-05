import json

def export_to_json(
    filename,
    target,
    response,
    analysis,
    score,
    risk_level

):

    """
    Export scan results to a JSON file.

    Args:
        filename (str): Output filename.
        target (str): Target URL.
        response (requests.Response): HTTP response.
        analysis (dict): Security analysis.
        score (int): Security score.
        risk_level (str): Risk level.
    """

    report = {
        "target": target,
        "final_url": response.url,
        "status_code": response.status_code,
        "score": score,
        "risk_level": risk_level,
        "analysis": analysis,

}

    with open(filename, "w",  encoding="utf-8")as file:
        json.dump(report, file, indent=4)

    print(f"\nReport saved to: {filename}")
