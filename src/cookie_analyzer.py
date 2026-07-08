"""
Cookie security analysis.

This module inspects the Set-Cookie headers returned by a response and
checks each cookie for the security attributes that matter most:
Secure, HttpOnly, SameSite, and an expiry (Expires or Max-Age).
"""


def _get_raw_cookies(response):
    """
    Extract every raw "Set-Cookie" header string from a response.

    A server can send multiple Set-Cookie headers in one response (one per
    cookie). requests' `response.headers` collapses repeated headers into a
    single comma-joined string, which is unsafe for Set-Cookie because cookie
    values (like Expires dates) can themselves contain commas. To avoid that,
    this reads the list straight from the underlying urllib3 response, which
    keeps each Set-Cookie header separate.

    Args:
        response (requests.Response): HTTP response.

    Returns:
        list[str]: Raw Set-Cookie header strings (possibly empty).
    """

    try:
        return response.raw.headers.getlist("Set-Cookie")

    except AttributeError:
        # Fallback for edge cases where response.raw isn't available.
        single = response.headers.get("Set-Cookie")
        return [single] if single else []


def _parse_cookie(raw_cookie):
    """
    Parse a single raw Set-Cookie header string into its name and
    attributes.

    Args:
        raw_cookie (str): Raw Set-Cookie header value,
            e.g. "session=abc123; Secure; HttpOnly; SameSite=Strict".

    Returns:
        dict: Parsed cookie attributes.
    """

    parts = [part.strip() for part in raw_cookie.split(";") if part.strip()]

    name = parts[0].split("=")[0] if parts else "(unknown)"
    attributes = parts[1:]

    secure = False
    httponly = False
    samesite = None
    has_expiry = False

    for attribute in attributes:
        lowered = attribute.lower()

        if lowered == "secure":
            secure = True

        elif lowered == "httponly":
            httponly = True

        elif lowered.startswith("samesite="):
            samesite = attribute.split("=", 1)[1]

        elif lowered.startswith("expires=") or lowered.startswith("max-age="):
            has_expiry = True

    return {
        "name": name,
        "secure": secure,
        "httponly": httponly,
        "samesite": samesite,
        "has_expiry": has_expiry,
        "raw": raw_cookie,
    }


def _evaluate_cookie(cookie):
    """
    Check a parsed cookie against basic security best practices.

    Args:
        cookie (dict): Parsed cookie from _parse_cookie().

    Returns:
        dict: The same cookie dict, plus "issues" (list[str]) and
            "status" ("Secure" or "Needs Attention").
    """

    issues = []

    if not cookie["secure"]:
        issues.append("Missing Secure flag (cookie can be sent over plain HTTP).")

    if not cookie["httponly"]:
        issues.append("Missing HttpOnly flag (cookie is readable by JavaScript).")

    if cookie["samesite"] is None:
        issues.append("Missing SameSite attribute (no CSRF protection).")

    elif cookie["samesite"].lower() == "none" and not cookie["secure"]:
        issues.append("SameSite=None requires the Secure flag to be set.")

    if not cookie["has_expiry"]:
        issues.append("No expiry set (session cookie — acceptable, but confirm this is intended).")

    cookie["issues"] = issues
    cookie["status"] = "Secure" if not issues else "Needs Attention"

    return cookie


def analyze_cookies(response):
    """
    Analyze all cookies set by a response.

    Args:
        response (requests.Response): HTTP response.

    Returns:
        list[dict]: One analysis result per cookie. Empty list if the
            response did not set any cookies.
    """

    raw_cookies = _get_raw_cookies(response)

    results = []

    for raw_cookie in raw_cookies:
        parsed = _parse_cookie(raw_cookie)
        evaluated = _evaluate_cookie(parsed)
        results.append(evaluated)

    return results
