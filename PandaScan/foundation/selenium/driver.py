import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from .utils import check_driver, check_extensions


def set_driver_config(MAIN_DIRECTORY, PATH_TO_CONFIG, SETTINGS, LOG):
    """Instantiate the browser elements.

    Args:
        MAIN_DIRECTORY (str): path to the working directory
        PATH_TO_CONFIG (str): path to the .json file
        SETTINGS (Any): .json configuration file
        LOG (Any): the logger

    Returns:
        Any: the webdriver
    """

    ublock_path = f'{MAIN_DIRECTORY}/foundation/selenium/extensions/ublock.crx'
    adguard_path = f'{MAIN_DIRECTORY}/foundation/selenium/extensions/adguard.crx'
    check_extensions(ublock_path, adguard_path)

    check_driver(SETTINGS['chromedriver_path'], PATH_TO_CONFIG, SETTINGS)

    # Instantiate chromedriver service
    chromedriver_path = Service(SETTINGS['chromedriver_path'])

    # Instantiate chrome options
    options = webdriver.ChromeOptions()
    if SETTINGS['driver']['headless']:
        options.add_argument("--headless")
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
        LOG.info("The path provided isn't the 'chromedriver.exe' file ⚠️ \n\nPlease refer to the 'README' file to provide the correct path.")
        LOG.debug({str(e)})
        SETTINGS["chromedriver_path"] = ""
        with open(PATH_TO_CONFIG, 'w') as json_file:
            json.dump(SETTINGS, json_file, indent=4)
        print("PandaScan exited. 🚪\n")
        exit()

    driver.maximize_window()
    print("\nChromeDriver found ✅")

    return driver
