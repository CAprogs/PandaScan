import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

links_list = []
manga_name_list = []

print("\nDébut Scrapping ...\n")

# Configuration de Selenium pour utiliser Chrome avec le profil
chrome_profile_path = '/Users/charles-albert/Library/Application Support/Google/Chrome/Default'
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + chrome_profile_path)
driver = webdriver.Chrome(options=options)          

# Ouvrir la page contennat tous les mangas
url = "https://fmteam.fr/comics"
driver.get(url)

# Attendre que le contenu soit chargé et que le JavaScript s'exécute
driver.implicitly_wait(10)  # Attente implicite

i = 1       # depart ( correpond au 1 er manga de la page )
while True:
    # récupérer les informations à partir du XPATH
    balise = str(f'//*[@id="app"]/main/div/div/div[2]/div[{i}]/div[2]/h5/a')
    try:
        element = driver.find_element(By.XPATH,balise)                   # récupérer l'élément correspondant au XPATH
        url_manga = element.get_attribute('href')                                # récupérer le lien du manga
        manga_name = url_manga.split("/")[-1]                                      # récupérer le nom du manga
        links_list.append(url_manga)
        manga_name_list.append(manga_name)
        i += 1
    except:
        print(f"Erreur au manga N°{i}, Fin Scrapping")
        break

print (len(manga_name_list)," mangas récupérés\n")

data_to_add = [{"name": name, "links": links} for name, links in zip(manga_name_list, links_list)]

datas = pd.DataFrame(data_to_add)

print(f"\nSauvegarde des datas ...")
datas.to_csv('/Users/charles-albert/Desktop/PandaScan/PandaScan/datas/fmteam.fr/mangas.csv', index=False)

print(f"\nFin.")

# Fermer le navigateur
driver.quit()