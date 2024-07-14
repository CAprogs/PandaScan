from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from .utils import check_driver, check_extensions, dump_config


def set_driver_config(OS_NAME: str, SRC_DIRECTORY: str, PATH_TO_CONFIG: str, SETTINGS, LOG, EMOJIS: dict):
    """Instantiate the browser elements.

    Args:
        OS_NAME (str): name of the OS
        SRC_DIRECTORY (str): path to the src directory
        PATH_TO_CONFIG (str): path to the .json file
        SETTINGS (Any): .json configuration file
        LOG (Any): the logger
        EMOJIS (dict): the emojis

    Returns:
        Any: the webdriver
    """

    ublock_path = f'{SRC_DIRECTORY}/foundation/selenium/extensions/ublock.crx'
    adguard_path = f'{SRC_DIRECTORY}/foundation/selenium/extensions/adguard.crx'
    check_extensions(ublock_path, adguard_path, EMOJIS)

    check_driver(OS_NAME, LOG, SETTINGS["driver"]["path"], PATH_TO_CONFIG, SETTINGS, SRC_DIRECTORY)

    # Instantiate chromedriver service
    chromedriver_path = Service(SETTINGS["driver"]["path"])

    # Instantiate chrome options
    options = webdriver.ChromeOptions()
    if SETTINGS['driver']['headless']:
        options.add_argument("--headless=new")
        options.add_argument(SETTINGS['driver']['user_agent'])
        LOG.debug("Browser mode : Headless")
    else:
        LOG.debug("Browser mode : Headed")

    # Add extensions
    options.add_extension(ublock_path)
    options.add_extension(adguard_path)

    # Instantiate the driver
    try:
        driver = webdriver.Chrome(service=chromedriver_path, options=options)
    except Exception as e:
        LOG.info("""The path provided is obsolete or doesn't refer to the 'chromedriver.exe' file ⚠️
                \nIf you previously downloaded the chromedriver, you might need to authorize its execution.
                \nIf the issue persists, please update your browser to the latest version by going to : chrome://settings/help
                \nRefer to the 'README' file for more information.
                """)
        LOG.debug({str(e)})
        SETTINGS["driver"]["path"] = ""
        dump_config(PATH_TO_CONFIG, SETTINGS)
        print(f"PandaScan exited. {EMOJIS[1]}\n")
        exit()

    if SETTINGS["driver"].get("downloaded_driver") is not None:
        SETTINGS["driver"].pop("downloaded_driver")
        dump_config(PATH_TO_CONFIG, SETTINGS)
    driver.maximize_window()
    print(f"\nChromeDriver found {EMOJIS[3]}")

    return driver
