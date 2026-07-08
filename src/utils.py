from pathlib import Path
from urllib.parse import urlparse

def load_targets(filename):
    """
    Load target URLs from a text file.

    Args:
        filename (str): Path to the target list.

    Returns:
        list[str]: List of target URLs.
    """

    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(f"Target file not found: {filename}")

    targets = []

    with path.open("r", encoding="utf-8")as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            targets.append(line)

    return targets

def create_report_directory(url, reports_dir="reports"):
    """
    Create a report directory for a target.

    Args:
        url (str): Target URL.
        reports_dir (str): Base folder to store reports in, read from
            config.ini.

    Returns:
        pathlib.Path: Report directory path.
    """

    domain = urlparse(url).netloc
    report_dir = Path(reports_dir) / domain
    report_dir.mkdir(
        parents=True,
        exist_ok=True,
)

    return report_dir
