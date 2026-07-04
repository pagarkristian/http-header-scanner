from src.scanner import scan_website
from src.analyzer import analyze_headers
from src.scoring import calculate_score
from src.constants import HEADER_INFORMATION
from src.display import (
    display_banner,
    display_headers,
    display_security_analysis,
    display_security_score,
    display_security_recommendations,
)


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
    display_security_analysis(analysis)
    score, risk_level = calculate_score(analysis)

    score, risk_level = calculate_score(analysis)
    display_security_score(score, risk_level)

    display_security_recommendations(
        analysis,
        HEADER_INFORMATION,
)

if __name__ == "__main__":
    main()













