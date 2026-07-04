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
        status = "Missing"
        value = "N/A"

        if present:
            status = "Present"
            value = headers.get(header)

        elif (
            header == "Content-Security-Policy"
            and "Content-Security-Policy-Report-Only" in headers

        ):

            status = "Report Only"
            value = headers.get("Content-Security-Policy-Report-Only")

        results[header] = {
            "present": present,
            "status": status,
            "value": value,

}


    return results
