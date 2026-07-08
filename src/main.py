import time
import argparse

from src.scanner import scan_website
from src.analyzer import analyze_headers
from src.cookie_analyzer import analyze_cookies
from src.scoring import calculate_score
from src.exporter import export_to_json
from src.html_report import generate_html_report
from src.constants import HEADER_INFORMATION
from src.config import load_config
from src.logger_config import setup_logger

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
    display_unexpected_error,
    display_headers,
    run_with_progress,
    display_security_analysis,
    display_cookie_analysis,
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
        description="Professional HTTP Security Header Scanner",
    )

    parser.add_argument(
        "url",
        nargs="?",
        help="Target Url To Scan"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="HTTP Header Scanner v3.8",
    )

    parser.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        help="Read target URLs from a text file",
    )

    return parser.parse_args()


def scan_target(url, config, logger):
    """
    Scan a single target and generate reports.

    Args:
        url (str): Target URL.
        config (configparser.ConfigParser): Application configuration.
        logger (logging.Logger): Application logger.
    """

    logger.info("Starting scan for %s", url)

    try:
        start_time = time.perf_counter()

        timeout = config["scanner"].getint("timeout", fallback=10)

        with scanning_status(url):
            response = scan_website(url, timeout=timeout)

        if response is None:
            display_scan_error(url)
            logger.warning("Scan returned no response for %s", url)
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

        cookies = run_with_progress(
            "Analyzing cookie security",
            analyze_cookies,
            response,
        )
        display_cookie_analysis(cookies)

        display_security_recommendations(
            analysis,
            HEADER_INFORMATION,
        )

        scan_duration = round(
            time.perf_counter() - start_time,
            2,
        )

        reports_dir = config["output"].get("reports_dir", fallback="reports")
        report_dir = create_report_directory(url, reports_dir=reports_dir)

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
                cookies,
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

        logger.info(
            "Finished scan for %s (score=%s, risk=%s, duration=%ss)",
            url, score, risk_level, scan_duration,
        )

    except Exception as error:
        # A broad catch is normally discouraged, but here it is the last
        # line of defense: any bug in analysis/export code should show
        # the user a clean message instead of crashing the whole batch
        # scan, while the real detail still goes to the log file.
        logger.exception("Unexpected error while scanning %s", url)
        display_unexpected_error(url, error)


def main():
    """
    Run the application.
    """

    config = load_config()

    logger = setup_logger(
        logs_dir=config["logging"].get("logs_dir", fallback="logs"),
        log_level=config["logging"].get("log_level", fallback="INFO"),
    )

    display_banner()

    args = parse_arguments()

    if args.file:
        targets = load_targets(args.file)

        console.print(f"\nLoaded {len(targets)} targets.\n")

        for target in targets:
            scan_target(target, config, logger)

        return

    if args.url:
        url = args.url
    else:
        url = console.input("\n[bold]Enter URL[/]: ").strip()

    scan_target(url, config, logger)

if __name__ == "__main__":
    main()

