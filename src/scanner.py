import requests

def scan_website(url):
    """
    Send an HTTP Get request to the target website
    Args:
        url(str): Target Website Url.
    Returns:
        requests.Response | none:
            Return a response object if the request succeeds.
            Return None if an error occurs.
    """

    try:
        response = requests.get(url, timeout=10)
        return response

    except requests.exceptions.RequestException as error:
        print(f"\n [error] {error}")
        return None
