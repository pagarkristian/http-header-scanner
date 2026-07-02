from src.scanner import scan_website
from src.analyzer import analyze_headers
from src.scoring import calculate_score
from src.constants import HEADER_INFORMATION


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


def main():
    """
    Run the application.
    """

    display_banner()

    url = input("\nEnter URL: ").strip()

    response = scan_website(url)

    if response is None:
        return

    print("\nRequest completed successfully.\n")

    print(f"Final URL   : {response.url}")
    print(f"Status Code : {response.status_code}")

    display_headers(response.headers)

    analysis = analyze_headers(response.headers)

    print("\nSecurity Analysis")
    print("-" * 50)

    for header, info in analysis.items():
        symbol = "✓" if info["present"] else "✗"

        print(f"[{symbol}] {header}")

        if info["present"]:
            print(f"    Value : {info['value']}")

    score, risk_level = calculate_score(analysis)

    print("\nSecurity Score")
    print("-" * 50)
    print(f"Score      : {score}/100")
    print(f"Risk Level : {risk_level}")

    print("\nSecurity Recommendations")
    print("-" * 50)

    for header, info in analysis.items():
        if not info["present"]:

            details = HEADER_INFORMATION[header]

            print(f"\n[!] {header}")
            print("Risk:")
            print(f"    {details['risk']}")
            print("Recommendation:")
            print(f"    {details['recommendation']}")


if __name__ == "__main__":
    main()
