# ---------------------------------------------- Obligatoire pour accéder aux modules du dossier principal
import sys
from Path_to_fmteam import script_repo,current_dir
sys.path.append(script_repo)
sys.path.append(current_dir)
# ----------------------------------------------
import pandas as pd
import yaml
import re
from selenium.webdriver.common.by import By
from Selenium_config import driver

def Scrap_Chapters():
    """Scrap the mangas chapters.
    """    
    
    print("\n Importation et Creation des données ... \n")
    datas = pd.read_csv(f'{script_repo}/datas/mangas.csv') # Accès mangas et liens
    manga_chapters_dict = {} # création du dictionnaire qui contiendra les chapitres respectifs de chaque manga

    print("\nDébut Scrapping ...\n")   

    pattern = r'/ch/(\d+)/sub/(\d+)' # servira de pattern pour la recherche

    for index, manga_name in enumerate(datas['name']):
        url = datas['links'][index]
        driver.get(url)

        # Attendre que le contenu soit chargé et que le JavaScript s'exécute
        driver.implicitly_wait(5)  # Attente implicite
        
        i = 2      # depart ( correpond au dernier chapitre de la page de téléchargement )
        print(f"\nManga : {manga_name}") # Indique dans quel manga nous sommes pour le scrapping des chapitres
        manga_chapters_dict[manga_name]=[] # Crée une clé de dictionnaire vide , avec le nom du manga qu'on explore.
        while True:
            # récupérer les informations à partir du XPATH
            balise = str(f'//*[@id="comic"]/div[3]/div[2]/div[{i}]/div[1]/a[1]')
            try:
                element = driver.find_element(By.XPATH,balise)                   # récupérer l'élément correspondant au XPATH
                url_chapter_download = element.get_attribute('href')                        # récupérer le lien du chapitre
                if "sub" in url_chapter_download:
                    matches = re.search(pattern, url_chapter_download)
                    if matches:
                        ch_number = matches.group(1)
                        sub_number = matches.group(2)
                        chapter_number = ch_number + "." + sub_number
                    else:
                        print("ERREUR, AUCUN MATCH")
                else:
                    chapter_number = url_chapter_download.split("/")[-1]                        # récupérer le numero de chapitre 

                chapter = "chapitre " + chapter_number                          # normaliser le chapitre
                manga_chapters_dict[manga_name].append(chapter)                 # Ajouter le chapitre à 'manga_chapters_dict' avec sa clé correspondante
                print(f"{chapter} récupéré ")
                i += 1
            except:
                print(f"\nChapitre N°{float(chapter_number)-1} INEXISTANT | {manga_name}\n")
                break

    # Convertir le dictionnaire en document YAML
    yml_data = yaml.dump(manga_chapters_dict)

    print(f"\nSauvegarde des datas ...")
    # Sauvegarde des datas
    with open(f'{script_repo}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)

    print(f"\nFin Scrapping.")


# Uncomment to debug
#if __name__ == "__main__":
    #Scrap_Chapters()
