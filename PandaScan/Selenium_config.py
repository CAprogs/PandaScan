from selenium import webdriver

# ----- Configuration de Selenium pour utiliser Chrome -----
# Chemin vers le profil Chrome
chrome_profile_path = '/Users/charles-albert/Library/Application Support/Google/Chrome/Default'  # Change this to your Chrome Profile path
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + chrome_profile_path)
driver = webdriver.Chrome(options=options)
driver.maximize_window() # Ouvrir le navigateur en full size
# -----------------------------------------------------------