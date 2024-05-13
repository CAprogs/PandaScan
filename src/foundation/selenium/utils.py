import json
import os
import time
import requests
import sys
import zipfile
import io
import platform


def clear_console():
    """Clear the console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def exit_app():
    """Exit the application.
    """
    clear_console()
    print("\nPandaScan exited. ⚠️\n")
    exit()


def dump_config(PATH_TO_CONFIG: str, SETTINGS):
    """Dump the new configuration.

    Args:
        PATH_TO_CONFIG (str): path to the config.json file
        SETTINGS (Any): the config.json file
    """
    with open(PATH_TO_CONFIG, 'w') as json_file:
        json.dump(SETTINGS, json_file, indent=4)


def check_extensions(extension_path_1: str, extension_path_2: str, EMOJIS):
    """Check the extensions presence.

    Args:
        extension_path_1 (str): path to extension 1
        extension_path_2 (str): path to extension 2
        EMOJIS (dict): the emojis
    """
    if not os.path.exists(extension_path_1) or not os.path.exists(extension_path_2):
        print(f"\nSome CRX extensions are missing. ⚠️\n\nPandaScan exited {EMOJIS[1]}")
        exit()
    else:
        print(f"\nExtensions found {EMOJIS[3]}")


def check_path(OS_NAME: str, path: str, interrupt: bool = False):
    """Check if the user-provided path is right and correct it if necessary.

    Args:
        OS_NAME (str): name of the OS
        path (str): the path to correct (if necessary)
        interrupt (bool, optional): whether the function should print a message or not. Defaults to False.

    Returns:
        str: the right path (depending on the OS) or an empty string if the path doesn’t exist
    """

    if not os.path.exists(path):
        if interrupt:
            print(f"\nPath '{path}' doesn’t exist.")
            time.sleep(2)
        return ""
    elif OS_NAME == "Windows":
        correct_path = path.replace("\\", "\\\\")
        return correct_path
    else:
        return path


def download_chromedriver(LOG, SETTINGS, SRC_DIRECTORY: str):
    """Download the latest ChromeDriver.

    Args:
        LOG (Any): the logger
        SETTINGS (Any): the config.json file
        SRC_DIRECTORY (str): path to the src directory

    Returns:
        str | None: the path to the downloaded chromedriver or None if the download failed
    """
    MAIN_DIRECTORY = f"{SRC_DIRECTORY}/.."
    interface = None
    processor = platform.processor()
    architecture = platform.architecture()
    os_platform = sys.platform

    try:
        response = requests.get(SETTINGS["driver"]["api_endpoint"])
    except requests.exceptions.RequestException as e:
        LOG.debug({str(e)})
        return None

    print("Downloading the latest ChromeDriver...")

    if response.status_code == 200:
        data = response.json()
        download_datas = data["channels"]["Stable"]["downloads"]["chromedriver"]

        if os_platform == 'win32' or os_platform == 'cygwin' or os_platform == 'msys':
            if architecture[0] == '64bit':
                interface = "win64"
            else:
                interface = "win32"
        elif os_platform == 'linux':
            interface = "linux64"
        elif os_platform == 'darwin':
            if processor == 'arm':
                interface = "mac-arm64"
            else:
                interface = "mac-x64"
        else:
            print("OS not supported ⚠️")
            return None

        chromedriver_url = [data["url"] for data in download_datas if data['platform'] == str(interface)]
        response = requests.get(chromedriver_url[0])

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(MAIN_DIRECTORY)
            files = zip_ref.namelist()

            for file in files:
                if 'LICENSE' not in file:
                    if "win" in interface and not file.endswith(".exe"):
                        file += ".exe"
                    driver_path = f"{MAIN_DIRECTORY}/{file}"

        if SETTINGS["driver"].get("downloaded_driver") is None:
            SETTINGS["driver"]["downloaded_driver"] = driver_path
        print(f"\nChromedriver downloaded at this location : {driver_path}")
        time.sleep(2.5)
        return driver_path
    else:
        LOG.debug(f"Download Failed with status code : {response.status_code}")
        return None


def provide_driver_path():
    """Provide the path to the chromedriver.

    Returns:
        str: the path to the chromedriver
    """
    try:
        driver_path = input("""
                \n° On macOS : just paste the path to the 'chromedriver' file (executable)
                \n° On Windows : include the '.exe' extension in the path (e.g. 'C:\\Users\\User\\chromedriver.exe')
                \n° On Linux with arm64 (VM) : consider downloading the Lite version of PandaScan instead

                \rPress CTRL + C to exit.
                \n\r          =>  """)
        return driver_path
    except KeyboardInterrupt:
        exit_app()


def check_driver(OS_NAME: str, LOG, driver_path: str, PATH_TO_CONFIG: str, SETTINGS, SRC_DIRECTORY: str):
    """Check the chromedriver’s presence.

    Args:
        OS_NAME (str): name of the OS
        LOG (Any): the logger
        driver_path (str): path to the 'chromedriver.exe' file
        PATH_TO_CONFIG (str): path to the config.json file
        SETTINGS (Any): the config.json file
        SRC_DIRECTORY (str): path to the src directory
    """

    if SETTINGS["driver"].get("downloaded_driver") is not None:
        driver_path = SETTINGS["driver"]["downloaded_driver"]

    while "chromedriver" not in driver_path or not os.path.exists(driver_path) or "LICENSE" in driver_path:

        menu_answer = None

        while menu_answer not in ["1", "2"]:
            clear_console()
            try:
                menu_answer = input("""ChromeDriver is required to run PandaScan. ⚠️  (Select the appropriate option below)
                        \n   [1] Provide the path to an existing ChromeDriver
                        \n   [2] Download and execute the latest ChromeDriver ( recommended )

                    \rPress CTRL + C to exit.
                    \n          =>  """)
                if menu_answer not in ["1", "2"]:
                    print("\nInvalid choice ⚠️, choose between 1 and 2.")
                    time.sleep(1.5)
            except KeyboardInterrupt:
                exit_app()

        clear_console()

        if menu_answer == "1":
            driver_path = provide_driver_path()
        elif menu_answer == "2":
            driver_path = download_chromedriver(LOG, SETTINGS, SRC_DIRECTORY)

        driver_path = check_path(OS_NAME, driver_path, True)

    SETTINGS["driver"]["path"] = driver_path
    if OS_NAME != "Windows":
        os.system("chmod +x " + driver_path)
    dump_config(PATH_TO_CONFIG, SETTINGS)

    clear_console()
