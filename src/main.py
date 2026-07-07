import time
import argparse

from src.scanner import scan_website
from src.analyzer import analyze_headers
from src.scoring import calculate_score
from src.exporter import export_to_json
from src.html_report import generate_html_report
from src.constants import HEADER_INFORMATION

from src.utils import (
    load_targets,
    create_report_directory,
)

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


def parse_arguments():
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        prog="http-header-scanner",
        description="Profesional HTTP Security Header Scanner",
    )

    parser.add_argument(
        "url",
        nargs="?",
        help="Target Url To Scan"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="HTTP Header Scanner v3.0",
    )

    parser.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="Read target URLs from a text file",
    )

    return parser.parse_args()


def scan_target(url):
    """
    Scan a single target and generate reports.

    Args:
        url (str): Target URL.
    """
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
        2,
    )

    report_dir = create_report_directory(url)

    json_path = report_dir / "report.json"
    html_path = report_dir / "report.html"

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


def main():
    """
    Run the application.
    """

    display_banner()

    args = parse_arguments()

    if args.file:
        targets = load_targets(args.file)

        console.print(f"\nLoaded {len(targets)} targets.\n")

        for target in targets:
            scan_target(target)

        return

    if args.url:
        url = args.url
    else:
        url = console.input("\n[bold]Enter URL[/]: ").strip()

    scan_target(url)

if __name__ == "__main__":
    main()

