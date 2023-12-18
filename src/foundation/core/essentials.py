import os
import platform
import requests
import json
import sqlite3 as sql
from tkinter import messagebox
from pathlib import Path
from ..selenium.driver import set_driver_config
from src.foundation.logger.log import CustomLogger, LOG_FORMATS
from .emojis import EMOJIS


# Get OS name
OS_NAME = platform.system()

# Cursor types
INACTIVE_CURSOR = "arrow"
ACTIVE_CURSOR = "hand2"

# Available websites
WEBSITES_DICT = {"fmteam": "FR",
                 "lelscans": "FR",
                 "animesama": "FR",
                 "scantrad": "FR",
                 "tcbscans": "EN",
                 "lelmanga": "FR"
                 }

# Available languages mode
LANGUAGES = ["All",
             EMOJIS[6],
             EMOJIS[7]]

# Set list of websites depending on their language
ALL_WEBSITES = [website for website in WEBSITES_DICT.keys()]
FR_WEBSITES = [website for website, lang in WEBSITES_DICT.items() if lang == "FR"]
EN_WEBSITES = [website for website, lang in WEBSITES_DICT.items() if lang == "EN"]

# Pandascan directory
MAIN_DIRECTORY = Path(os.path.abspath(os.getcwd()))

# Src directory
SRC_DIRECTORY = MAIN_DIRECTORY / "src"

# Assets directory
ASSETS_DIRECTORY = SRC_DIRECTORY / "gui/assets"

# Path to config file
PATH_TO_CONFIG = SRC_DIRECTORY / "config.json"

# paths to websites file ( Update )
PATH_TO_SCANTRAD = SRC_DIRECTORY / "update/websites/scantrad"
PATH_TO_LELSCANS = SRC_DIRECTORY / "update/websites/lelscans"
PATH_TO_FMTEAM = SRC_DIRECTORY / "update/websites/fmteam"
PATH_TO_ANIMESAMA = SRC_DIRECTORY / "update/websites/animesama"
PATH_TO_TCBSCANS = SRC_DIRECTORY / "update/websites/tcbscans"
PATH_TO_LELMANGA = SRC_DIRECTORY / "update/websites/lelmanga"

# load config file
with open(PATH_TO_CONFIG) as json_file:
    SETTINGS = json.load(json_file)

# Set the default websites
if SETTINGS["websites"]["languages"] == "All":
    WEBSITES = ALL_WEBSITES
elif SETTINGS["websites"]["languages"] == "FR":
    WEBSITES = FR_WEBSITES
elif SETTINGS["websites"]["languages"] == "EN":
    WEBSITES = EN_WEBSITES

# Instanciate the logger
if SETTINGS["logger"]["enabled"] is False:
    LOG = CustomLogger(state=False)  # Disable debug and info logs
elif SETTINGS["logger"]["enabled"] is True and SETTINGS["logger"]["level"] == "DEBUG":
    LOG = CustomLogger(level="DEBUG", format=LOG_FORMATS[1])  # Display all logs
elif SETTINGS["logger"]["enabled"] is True and SETTINGS["logger"]["level"] == "INFO":
    LOG = CustomLogger(format=LOG_FORMATS[0])  # Only Display info logs

# Configure chromedriver and selenium
DRIVER = set_driver_config(OS_NAME, SRC_DIRECTORY, PATH_TO_CONFIG, SETTINGS, LOG, EMOJIS)

# Load SQl datas
try:
    CONN = sql.connect(f'{SRC_DIRECTORY}/foundation/database/Pan_datas.db')
    SELECTOR = CONN.cursor()
    print(f"\nDatas Loaded {EMOJIS[3]}")
except sql.Error as e:
    messagebox.showinfo(f"Database Error [{EMOJIS[15]}]", f"{EMOJIS[9]} Oups, the database is missing. {EMOJIS[17]}\n Error: {str(e)}")
    exit()


def check_connection():
    """Check if an internet connection is established.

    Returns:
        bool: True (connected to the internet), False (otherwise)
    """

    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            print(f"\nConnected to Internet {EMOJIS[3]}\n")
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"\n{e}\n")


def check_version():
    """Check if app's version is the latest
    """

    filters = [".", "v"]
    try:
        response = requests.get("https://api.github.com/repos/CAprogs/PandaScan/releases/latest")
    except requests.RequestException as e:
        print(f"\n{e}\n")
        return

    try:
        if response.status_code == 200:
            release_info = response.json()
            latest_version = release_info['tag_name'].replace("-beta", "")
            current_version = SETTINGS["App_version"]
            str_latest_v = latest_version
            str_current_v = current_version
            for filter in filters:
                latest_version = latest_version.replace(filter, "")
                current_version = current_version.replace(filter, "")

            if int(latest_version) > int(current_version):
                messagebox.showinfo(f"App's Update [{EMOJIS[8]}]", f"""
                                    A new version of Pandascan is available !

                                    latest : {str_latest_v}
                                    current : {str_current_v}

                                    https://github.com/CAprogs/PandaScan/releases""")
            elif int(latest_version) == int(current_version):
                LOG.info(f"App's up-to-date {EMOJIS[3]}")
        else:
            LOG.debug(f"An error occured {EMOJIS[9]}, status code : {response.status_code}")
    except Exception as e:
        LOG.debug(f"Error : {e}")


def relative_to_assets(path: str) -> Path:
    """Get the relative path to the assets folder.

    Args:
        path (str): asset’s name with its extension (e.g. "logo.png")

    Returns:
        str: the relative path to the asset
    """

    return ASSETS_DIRECTORY / Path(path)
