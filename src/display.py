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
        if info["status"] == "Present":
            symbol = "✓"

        elif info["status"] == "Report Only":
            symbol = "!"

        else:
            symbol = "✗"

        print(f"[{symbol}] {header}")
        print(f"    Status : {info['status']}")

        if info["value"] !=  "N/A":
            print(f"    Value : {info['value']}")

def display_security_score(score, risk_level):
    """
    Display the security score.

    Args:
        score (int): Security score.
        risk_level (str): Risk level.
    """

    print("\nSecurity Score")
    print("-" * 50)
    print(f"Score      : {score}/100")
    print(f"Risk Level : {risk_level}")

def display_security_recommendations(analysis, header_information):
    """
    Display security recommendations.

    Args:
        analysis (dict): Security analysis results.
        header_information (dict): Security header information.
    """
    print("\nSecurity Recommendations")
    print("-" * 50)

    for header, info in analysis.items():

        if not info["present"]:
            details = header_information[header]

            print(f"\n[!] {header}")
            print("Risk:")
            print(f"    {details['risk']}")
            print("Recommendation:")
            print(f"    {details['recommendation']}")

