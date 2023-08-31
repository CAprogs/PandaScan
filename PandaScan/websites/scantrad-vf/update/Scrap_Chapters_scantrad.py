# ---------------------------------------------- Obligatoire pour accéder aux modules du dossier principal
import sys
from Path_to_scantrad import script_repo
sys.path.insert(0, script_repo)
# ----------------------------------------------
import pandas as pd
import re
import yaml
from selenium.webdriver.common.by import By
from Selenium_config import driver


def Scrap_Chapters():

    print("\n Importation et Création des données ... \n")
    # Ouvrir le fichier csv mangas
    datas = pd.read_csv(f'{script_repo}/datas/mangas.csv') # Parcourir les noms de mangas 
    manga_chapters_dict = {} # création du dictionnaire qui contiendra les chapitres respectifs de chaque manga

    print("\nDebut Scrapping ... ")
    for manga_name in datas['name']:

        url_start = f'https://scantrad-vf.co/manga/{manga_name}/'
        # Accès à la page avec Selenium
        driver.get(url_start)
        try:
            i = 1
            print(f"\nManga : {manga_name}") # Indique dans quel manga nous sommes pour le scrapping des chapitres
            manga_chapters_dict[manga_name]=[] # Crée une clé de dictionnaire vide , avec le nom du manga qu'on explore.       
            driver.implicitly_wait(2)   # Attendre que la page soit complètement chargée (vous pouvez ajuster le délai selon vos besoins)
            while True:
                try:
                    balise = str(f'//*[@id="manga-chapters-holder"]/div[2]/div/ul/li/ul/li/ul/li[{i}]/a')  # Récupérer l'élément qui contient le dernier chapitre 
                    element = driver.find_element(By.XPATH, balise) # Chemin vers la balise contenant le chapitre {i}
                    valeur_href = element.get_attribute('href') # Récupérer la valeur de l'attribut "href" de l'élément <a>
                    # Utiliser une expression régulière pour extraire la valeur
                    result = re.search(rf'/{manga_name}/([^/]+)/', valeur_href)  # On récupère le chapitre
                    if result:
                        chapter = result.group(1)
                        if chapter:
                            chapter_str = chapter.replace('-',' ')
                            manga_chapters_dict[manga_name].append(chapter_str)          # Ajouter le chapitre à 'manga_chapters_dict' avec sa clé correspondante   
                            print(f"{chapter_str} récupéré ")
                            i += 1
                        else:
                            print(f"Aucune valeur trouvée | chapter")
                            break
                    else:
                        print("Aucune valeur trouvée. | result")
                        break
                except:
                    break        
        except:
            print(f"Aucun chemin trouvé. | try")

    # Réinitialiser les index du dataframe
    datas = datas.reset_index(drop=True)
    # Convertir le dictionnaire en document YAML
    yml_data = yaml.dump(manga_chapters_dict)

    print("\nSauvegarde des datas ...")
    # Sauvegarde des datas
    datas.to_csv(f'{script_repo}/datas/mangas.csv', index=False)

    with open(f'{script_repo}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)

    print(f"\nFin Scrapping.")
    driver.quit()