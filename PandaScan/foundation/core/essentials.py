import os
import requests
import json
import sqlite3 as sql
from tkinter import messagebox
from pathlib import Path
from ..selenium.driver import set_driver_config
from foundation.logger.log import CustomLogger, LOG_LEVELS, LOG_FORMATS

# Cursor types
INACTIVE_CURSOR = "arrow"
ACTIVE_CURSOR = "hand2"

# Available websites
WEBSITES = ["fmteam",
            "lelscans",
            "animesama",
            "scantrad"
            ]

LEVELS = ["DEBUG", "INFO"]

# Working directory
MAIN_DIRECTORY = Path(os.path.abspath(os.getcwd()))

# Assets directory
ASSETS_DIRECTORY = MAIN_DIRECTORY / "gui/assets"

# Path to config file
PATH_TO_CONFIG = MAIN_DIRECTORY / "config.json"

# paths to websites file ( Update )
PATH_TO_SCANTRAD = MAIN_DIRECTORY / "update/websites/scantrad"
PATH_TO_LELSCANS = MAIN_DIRECTORY / "update/websites/lelscans"
PATH_TO_FMTEAM = MAIN_DIRECTORY / "update/websites/fmteam"
PATH_TO_ANIMESAMA = MAIN_DIRECTORY / "update/websites/animesama"

# load config file
with open(PATH_TO_CONFIG) as json_file:
    SETTINGS = json.load(json_file)

# Instanciate logger
if SETTINGS["logger"]["enabled"] is False:
    None
elif SETTINGS["logger"]["enabled"] is True and SETTINGS["logger"]["level"] == LEVELS[0]:
    LOG = CustomLogger(LOG_LEVELS[0], LOG_FORMATS[1])  # Display all messages
elif SETTINGS["logger"]["enabled"] is True and SETTINGS["logger"]["level"] == LEVELS[1]:
    LOG = CustomLogger(LOG_LEVELS[1], LOG_FORMATS[0])  # Only Display info messages

# Configure chromedriver and selenium
DRIVER = set_driver_config(MAIN_DIRECTORY, PATH_TO_CONFIG, SETTINGS, LOG)

# Load SQl datas
try:
    CONN = sql.connect(f'{MAIN_DIRECTORY}/foundation/database/Pan_datas.db')
    SELECTOR = CONN.cursor()
    print("\nDatas Loaded ✅")
except sql.Error as e:
    messagebox.showinfo("Error [📊]", f"😵‍💫 Oups, the database is missing. 🚨\n Error: {str(e)}")
    exit()


def check_connection():
    """Check if an internet connection is established.

    Returns:
        bool: True (connected to the internet), False (otherwise)
    """

    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            print("\nConnected to Internet ✅\n")
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"\n{e}\n")


def relative_to_assets(path: str) -> Path:
    """Get the relative path to the assets folder.

    Args:
        path (str): name of the asset

    Returns:
        str: the relative path to the asset
    """

    return ASSETS_DIRECTORY / Path(path)
