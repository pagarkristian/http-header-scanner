from src.scanner import scan_website
from src.analyzer import analyze_headers

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

    url = input("\nEnter URL: ").strip ()
    response = scan_website(url)

    if response is None:
        return
    print("\n Request completed successfully. \n")
    print(f"Final URL: {response.url}")
    print(f"Status Code : {response.status_code}")

    display_headers(response.headers)

    analysis = analyze_headers(response.headers)

    print("\n Security Analysis")
    print("-" * 50)

    for header, info in analysis.items():
        symbol = "✓" if info["present"] else "✗"

        print(f"[{symbol}] {header}")

        if info["present"]:
            print(f"    value : {info['value']}")

if __name__== "__main__":
    main()
