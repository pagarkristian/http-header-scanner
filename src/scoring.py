def calculate_score(analysis):
    """
    Calculate the security score.

    Args:
        analysis (dict): Security analysis results.

    Returns:
        tuple: (score, risk_level)
    """

    total_headers = len(analysis)
    present_headers = 0

    for info in analysis.values():
        if info["present"]:
            present_headers += 1

    score = round((present_headers / total_headers) * 100)

    if score >= 80:
        risk_level = "Low"

    elif score >= 50:
        risk_level = "Medium"

    else:
        risk_level = "High"

    return score, risk_level

