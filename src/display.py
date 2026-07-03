"""
Display functions for the HTTP Header Scanner.
"""

def display_banner():
    """
    Display the application banner.
    """

    print("=" * 50)
    print("HTTP Header Scanner v1.5")
    print("=" * 50)

def display_headers(headers):
    """
    Display all HTTP response headers.

    Args:
        headers (dict): HTTP response headers.
    """

    print("\nResponse Headers")
    print("-" * 50)

    for key, value in headers.items():
        print(f"{key:<30}: {value}")

def display_security_analysis(analysis):
    """
    Display the security header analysis.

    Args:
        analysis (dict): Security analysis results.
    """

    print("\nSecurity Analysis")
    print("-" * 50)

    for header, info in analysis.items():
        symbol = "✓" if info["present"] else "✗"

        print(f"[{symbol}] {header}")

        if info["present"]:
            print(f"    Value : {info['value']}")
