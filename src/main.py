from src.scanner import scan_website

def display_banner():
    """
    Display the application banner.
    """

    print("=" * 50)
    print("HTTP HEADER SCANNER V1.0")
    print("=" * 50)

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

if __name__== "__main__":
    main()
