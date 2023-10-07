import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pathlib import Path
from tkinter import messagebox

def check_extensions(extension_path_1,extension_path_2):
    """Vérifier si les fichiers CRX sont présent

    Args:
        extension_path_1 (str): chemin vers l'extension 1
        extension_path_2 (str): chemin vers l'extension 2
    """        
    if not os.path.exists(extension_path_1) or not os.path.exists(extension_path_2):
        messagebox.showerror("Error [😥]", "Some CRX extensions are missing. ⚠️ | Check 'Extensions' file.")
        print("\nExiting ..\n")                     ##### Track activity
        exit()  # Sortir du script
    else:
        print("\nExtensions found ✅")              ##### Track activity

def check_driver(driver_path):
    """Vérifier si le chemin vers l'EXE est valide.

    Args:
        driver_path (str): chemin vers l'exécutable du driver
    """ 
    if not driver_path or not os.path.exists(driver_path): 
        messagebox.showerror("Error [🤖❓]", "Incorrect or missing Chromedriver path. ⚠️ | Check 'Installation Guide'.")
        print("\nExiting ..\n")                      ##### Track activity                                                       ##################### Au lieu d'exit , demander dans une barre le chemin jusqu'à en avoir un valide
        exit()  # Sortir du script
    else:
        print("\nChromeDriver found ✅")            ##### Track activity

# ============================ Selenium configuration to use ChromeDriver ============================

# Charger les paramètres de configuration de l'application
with open('config.json') as config_file:
    config = json.load(config_file)

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# Chemin vers les fichiers CRX des extensions
ublock_path = f'{script_directory}/extensions/ublock.crx'
adguard_path = f'{script_directory}/extensions/adguard.crx'
check_extensions(ublock_path,adguard_path)

check_driver(config['chromedriver_path'])
# Récupérer le chemin vers le Chromedriver
chromedriver_path = Service(config['chromedriver_path'])

options = webdriver.ChromeOptions()
if config['driver']['headless']:
    options.add_argument("--headless")  # Ajouter l'option headless au navigateur
    print("\nBrowser [ mode : Headless ] waiting for orders 🐼.. !")                                        ##### Track activity
else:
    print("\nBrowser [ mode : Head (Test) ] waiting for orders 🐼.. !")                                            ##### Track activity 
options.add_extension(ublock_path)  # Ajouter ublock au navigateur
options.add_extension(adguard_path) # Ajouter adguard au navigateur

# Instanciation du navigateur avec les options
driver = webdriver.Chrome(service=chromedriver_path, options=options)
driver.maximize_window() # Ouvrir le navigateur en full size