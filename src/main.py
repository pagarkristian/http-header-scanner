from src.scanner import scan_website

def display_banner():
    """
    Display the application banner.
    """

    print("=" * 50)
    print("HTTP HEADER SCANNER V1.1")
    print("=" * 50)

def display_headers(headers):
    """
    Display all HTTP response headers.

    Args:
        headers (dict): HTTP response headers.
    """

    print("\nResponse Headers")
    print("-" * 50 )

    for key, value in headers.items():
        print(f"{key:<30}: {value}")


def main():
    """
    Run the application
    """

    display_banner()

    url = input("\nEnter URL : ").strip ()
    response = scan_website(url)

    if response is None:
        return
    print("\n Request completed successfully. \n")
    print(f"Final Url: {response.url}")
    print(f"Status Code : {response.status_code}")

    display_headers(response.headers)


if __name__== "__main__":
    main()
