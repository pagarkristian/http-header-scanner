from src.constants import HEADER_WEIGHTS

def calculate_score(analysis):
    """
    Calculate the security score.

    Args:
        analysis (dict): Security analysis results.

    Returns:
        tuple:
            score (int)
            risk_level (str)
    """

    score = 0

    for header, info in analysis.items():
        weight = HEADER_WEIGHTS[header]

        if info["status"] == "Present":
            score += weight

        elif info["status"] == "Report Only":
            score += weight * 0.5

    score = round(score)

    if score >= 90:
        risk_level = "Low"

    elif score >= 70:
        risk_level = "Medium"

    elif score >= 40:
        risk_level = "High"

    else:
        risk_level = "Critical"

    return score, risk_level
