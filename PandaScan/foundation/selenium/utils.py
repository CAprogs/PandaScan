import json
import os


def check_extensions(extension_path_1, extension_path_2, EMOJIS):
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


def check_path(OS_NAME, LOG, path):
    """Check if the user-provided path is right and correct it if necessary.

    Args:
        OS_NAME (str): name of the OS
        LOG (Any): the logger
        path (str): the path to correct (if necessary)

    Returns:
        str: the right path (depending on the OS) or an empty string if the path doesn’t exist
    """

    if not os.path.exists(path):
        LOG.debug(f"Path '{path}' doesn’t exist.")
        return ""
    elif OS_NAME == "Windows":
        correct_path = path.replace("\\", "\\\\")
        return correct_path
    else:
        return path


def check_driver(OS_NAME, LOG, driver_path, PATH_TO_CONFIG, SETTINGS):
    """Check the chromedriver’s presence.

    Args:
        OS_NAME (str): name of the OS
        LOG (Any): the logger
        driver_path (str): path to the 'chromedriver.exe' file
        PATH_TO_CONFIG (str): path to the config.json file
        SETTINGS (Any): the config.json file
    """

    while "chromedriver" not in driver_path or not os.path.exists(driver_path):

        os.system("clear")
        print("""\nChromeDriver is required to run PandaScan. ⚠️ (Refer to the 'README' file)
              \n° On Windows : include the '.exe' extension in the path (e.g. 'C:\\Users\\User\\chromedriver.exe')
              \n° On Linux with arm64 (VM) : consider downloading the Lite version instead""")
        driver_path = input("""\n             Insert your ChromeDriver's path here => """)

    driver_path = check_path(OS_NAME, LOG, driver_path)

    SETTINGS["driver"]["path"] = driver_path

    with open(PATH_TO_CONFIG, 'w') as json_file:
        json.dump(SETTINGS, json_file, indent=4)

    os.system("clear")
