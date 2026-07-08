"""
Application configuration.

Settings that a user might reasonably want to change (timeouts, output
folders, logging) live in config.ini instead of being hardcoded in the
source. If config.ini does not exist yet, one is created automatically
with sensible defaults, so the app still works on a first run.
"""

import configparser
from pathlib import Path


CONFIG_PATH = Path("config.ini")

DEFAULTS = {
    "scanner": {
        "timeout": "10",
    },
    "output": {
        "reports_dir": "reports",
    },
    "logging": {
        "logs_dir": "logs",
        "log_level": "INFO",
    },
}


def _create_default_config():
    """
    Write a config.ini file populated with the default values in
    DEFAULTS. Called automatically the first time the app runs without
    an existing config.ini.
    """

    parser = configparser.ConfigParser()

    for section, options in DEFAULTS.items():
        parser[section] = options

    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        parser.write(file)


def load_config():
    """
    Load application settings from config.ini, creating the file with
    default values first if it does not exist yet.

    Returns:
        configparser.ConfigParser: Parsed configuration. Values are
            accessed like `config["scanner"]["timeout"]` and are always
            strings — convert with `.getint()` / `.getboolean()` etc.
            when a different type is needed.
    """

    if not CONFIG_PATH.exists():
        _create_default_config()

    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH)

    return parser
