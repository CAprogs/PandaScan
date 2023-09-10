# ---------------------------------------------- Obligatoire pour accéder aux modules du dossier principal
import sys
from Path_to_scantrad import script_repo,current_dir
sys.path.append(script_repo)
sys.path.append(current_dir)
# ----------------------------------------------
import pandas as pd
import re
from selenium.webdriver.common.by import By
from Selenium_config import driver

def Scrap_Titles():

    starting_page = 1
    a = ""
    page = 1
    datas = pd.DataFrame(columns=["name"]) # on crée un dataframe d'une colonne
    new_list = [] # création d'une liste vide

    print("\n Debut Scrapping ... \n")
    while True:
        try:
            if starting_page == 1:
                url_start = f"https://scantrad-vf.co/manga/{a}?m_orderby=alphabet" # url page
            else:
                url_start = f"https://scantrad-vf.co/manga/page/{page}/?m_orderby=alphabet" # url page

            # Accès à la page avec Selenium
            driver.get(url_start)

            print(f"\n Page {starting_page} :")

            # on récupère tous les éléments correspondant à la classe 'h5'
            elements = driver.find_elements(By.CLASS_NAME, 'h5') 
            # Parcourir la liste des éléments de la classe h5
            for element in elements:
                link = element.find_element(By.TAG_NAME, 'a')
                # Récupérer la valeur de l'attribut "href" de l'élément <a>
                valeur_href = link.get_attribute('href')
                # Utiliser une expression régulière pour extraire uniquement le nom du manga 
                result = re.search(r'/manga/([^/]+)/', valeur_href)
                if result:
                    manga_name = result.group(1)
                    new_list.append({"name": manga_name})
                    print(f"{manga_name} ajouté")
                else:
                    print(f"Aucune valeur trouvée pour {valeur_href}. Page N°{starting_page}")
            starting_page += 1
            page += 1
        except:
            print("Fin Scrapping")
            break
            
    print(f"\n{len(new_list)} Récupérés.")
    # On ajoute le contenu de 'new_list' au dataframe 'datas'
    datas = pd.concat([datas, pd.DataFrame(new_list)], ignore_index=True)

    print(f"\nSauvegarde des datas ...")
    # Sauvegarde des datas
    datas.to_csv(f'{script_repo}/datas/mangas.csv', index=False)

    print(f"\nFermeture navigateur.")
    # Fermeture du navigateur
    driver.quit()


# Uncomment to debug
'''
if __name__ == "__main__":
    Scrap_Titles()
'''