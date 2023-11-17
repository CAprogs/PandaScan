import json
import os
import platform


def check_extensions(extension_path_1, extension_path_2):
    """Vérifier la présence des extensions.

    Args:
        extension_path_1 (str): chemin vers l'extension 1
        extension_path_2 (str): chemin vers l'extension 2
    """
    if not os.path.exists(extension_path_1) or not os.path.exists(extension_path_2):
        print("\nSome CRX extensions are missing. ⚠️\n\nPandaScan exited 🚪")
        exit()
    else:
        print("\nExtensions found ✅")


def check_driver(driver_path, PATH_TO_CONFIG, SETTINGS):
    """vérifier la présence du driver.

    Args:
        driver_path (str): chemin vers le driver
        SETTINGS (Any): fichier de configuration .json
    """
    os_name = platform.system()

    while "chromedriver" not in driver_path or not os.path.exists(driver_path):

        os.system("clear")
        print("""\nChromeDriver is required to run PandaScan. ⚠️ (Refer to the 'README' file for help)
              \n° On Windows : replace all '\\' with '\\\\'
              \n° On Linux with arm64 (VM) : consider downloading the Lite version instead""")
        driver_path = input("""\n             Insert your ChromeDriver path here => """)

    if os_name == "Windows":
        driver_path = driver_path.replace("\\", "\\\\")

    SETTINGS["chromedriver_path"] = driver_path

    with open(PATH_TO_CONFIG, 'w') as json_file:
        json.dump(SETTINGS, json_file, indent=4)

    os.system("clear")
    print("\nChromeDriver found ✅")
