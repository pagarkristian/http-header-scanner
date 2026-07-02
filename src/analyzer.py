from src.constants import SECURITY_HEADERS

def analyze_headers(headers):
    """
    Analyze security headers.

    Args:
        headers (dict): HTTP response headers.

    Returns:
        dict: Security header analysis results.
    """

    results = {}

    for header in SECURITY_HEADERS:

        present = header in headers
        results[header] ={
            "present": present,
            "value": headers.get(header, "N/A")
        }

    return results
