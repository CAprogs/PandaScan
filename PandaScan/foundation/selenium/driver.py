from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tkinter import messagebox
from .utils import check_driver, check_extensions


def set_driver_config(MAIN_DIRECTORY, PATH_TO_CONFIG, SETTINGS, LOG):
    """Instancier les élémnents du navigateur.

    Args:
        MAIN_DIRECTORY (str): chemin vers le working directory
        PATH_TO_CONFIG (str): chemin vers le fichier .json
        SETTINGS (Any): fichier de configuration .json
        LOG (Any): logger d'affichage
    """

    ublock_path = f'{MAIN_DIRECTORY}/foundation/selenium/extensions/ublock.crx'
    adguard_path = f'{MAIN_DIRECTORY}/foundation/selenium/extensions/adguard.crx'
    check_extensions(ublock_path, adguard_path)

    check_driver(SETTINGS['chromedriver_path'], PATH_TO_CONFIG, SETTINGS)

    try:
        # Instanciate chromedriver service
        chromedriver_path = Service(SETTINGS['chromedriver_path'])
    except Service.ServiceException as e:
        messagebox.showerror("Error [😥]", f"Chromedriver not found. ⚠️ | Follow the README file\nError: {str(e)}")
        print("\nPandaScan exited. 🚪")
        exit()

    # Instanciate chrome options
    options = webdriver.ChromeOptions()
    if SETTINGS['driver']['headless']:
        options.add_argument("--headless")
        LOG.debug("Browser mode : Headless")
    else:
        LOG.debug("Browser mode : Headed")

    # Add extensions
    options.add_extension(ublock_path)
    options.add_extension(adguard_path)

    # Instanciate driver
    driver = webdriver.Chrome(service=chromedriver_path, options=options)
    driver.maximize_window()

    return driver
