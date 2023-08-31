from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import json
import os

# ----- Configuration de Selenium pour utiliser ChromeWebdriver -----

# Charger le contenu du fichier config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# Chemin vers les fichiers CRX des extensions
ublock_path = f'{script_directory}/extensions/ublock.crx'
adguard_path = f'{script_directory}/extensions/adguard.crx'
chromedriver_path = Service(config['chromedriver_path'])

options = webdriver.ChromeOptions()
if config['driver']['headless']:
    options.add_argument("--headless")  # Ajouter l'option headless au navigateur
options.add_extension(ublock_path)  # Ajouter ublock au navigateur
options.add_extension(adguard_path) # Ajouter adguard au navigateur

# Instanciation du navigateur avec les options
driver = webdriver.Chrome(service=chromedriver_path, options=options)
driver.maximize_window() # Ouvrir le navigateur en full size

if config['driver']['headless']:
    print("\nNavigateur [ Headless ] en attente d'ordre .. !")
else:
    print("\nNavigateur en attente d'ordre .. !")
    
# -----------------------------------------------------------