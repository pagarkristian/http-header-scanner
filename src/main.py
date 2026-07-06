import time


from src.scanner import scan_website
from src.analyzer import analyze_headers
from src.scoring import calculate_score
from src.exporter import export_to_json
from src.html_report import generate_html_report
from src.constants import HEADER_INFORMATION

from src.display import (
    console,
    display_banner,
    scanning_status,
    saving_status,
    display_scan_success,
    display_scan_error,
    display_headers,
    run_with_progress,
    display_security_analysis,
    display_security_score,
    display_security_recommendations,
    display_scan_summary,
)


def main():
    """
    Run the application.
    """

    display_banner()

    url = console.input("\n[bold]Enter URL[/]: ").strip()

    start_time = time.perf_counter()

    with scanning_status(url):
        response = scan_website(url)

    if response is None:
        display_scan_error(url)
        return

    display_scan_success(response)

    display_headers(response.headers)

    analysis = run_with_progress(
        "Analyzing security headers",
        analyze_headers,
        response.headers,
    )
    display_security_analysis(analysis)

    score, risk_level = run_with_progress(
        "Calculating security score",
        calculate_score,
        analysis,
    )
    display_security_score(score, risk_level)

    display_security_recommendations(
        analysis,
        HEADER_INFORMATION,
    )

    scan_duration = round(
        time.perf_counter() - start_time,
        2
    )

    json_path = "reports/report.json"
    html_path = "reports/report.html"

    with saving_status():
        export_to_json(
            json_path,
            url,
            response,
            analysis,
            score,
            risk_level,
            scan_duration,
        )

        generate_html_report(
            json_path,
            html_path,
        )

    display_scan_summary(
        url,
        response,
        score,
        risk_level,
        scan_duration,
        json_path,
        html_path,
    )


if __name__ == "__main__":
    main()
