import time


from src.scanner import scan_website
from src.analyzer import analyze_headers
from src.scoring import calculate_score
from src.exporter import export_to_json
from src.html_report import generate_html_report
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

    start_time = time.perf_counter()

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
    display_security_score(score, risk_level)

    display_security_recommendations(
        analysis,
        HEADER_INFORMATION,
    )

    scan_duration = round(
        time.perf_counter() - start_time,
        2
    )

    export_to_json(
        "reports/report.json",
        url,
        response,
        analysis,
        score,
        risk_level,
        scan_duration,
    )

    generate_html_report(
        "reports/report.json",
        "reports/report.html",

    )


if __name__ == "__main__":
    main()
