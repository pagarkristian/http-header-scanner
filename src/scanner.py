import requests

from src.logger_config import get_logger


logger = get_logger()


def scan_website(url, timeout=10):
    """
    Send an HTTP GET request to the target website.

    Args:
        url (str): Target website URL. If no scheme is given, "https://"
            is assumed.
        timeout (int): Request timeout in seconds, read from config.ini.

    Returns:
        requests.Response | None:
            Return a response object if the request succeeds.
            Return None if an error occurs.
    """

    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    try:
        response = requests.get(url, timeout=timeout)
        return response

    except requests.exceptions.RequestException as error:
        print(f"\n [error] {error}")
        logger.error("Scan failed for %s: %s", url, error)
        return None
