# ---------------------------------------------- Obligatoire pour accéder aux modules du dossier principal
import sys
from Path_to_fmteam import script_repo,current_dir
sys.path.append(script_repo)
sys.path.append(current_dir)
# ----------------------------------------------

def Scrap_Titles():
    """Scrap the mangas titles.
    """
    import pandas as pd
    import re
    from selenium.webdriver.common.by import By
    from Selenium_config import driver
    
    manga_name_list = []    
    links_list = []
    has_tome_list = []
    last_tome_list = []

    print("\nDébut Scrapping ...\n")        

    # Ouvrir la page contenant tous les mangas
    url = "https://fmteam.fr/comics"

    try:
        driver.get(url)
        
        driver.implicitly_wait(2)  # Attendre que le contenu soit chargé et que le JavaScript s'exécute

        i = 1       # depart ( correspond au 1 er manga de la page )
        while True:
            balise_1 = str(f'//*[@id="app"]/main/div/div/div[2]/div[{i}]/div[2]/h5/a') # Balise du nom du manga
            balise_2 = str(f'//*[@id="app"]/main/div/div/div[2]/div[{i}]/ul/li[4]/a') # Balise du nom du Tome ou Chapitre
            try:
                element_1 = driver.find_element(By.XPATH,balise_1)                      # récupérer l'élément de la balise 1
                element_2 = driver.find_element(By.XPATH,balise_2).text                 # récupérer l'élément de la balise 2
                # Action 1
                url_manga = element_1.get_attribute('href')                    # récupérer le lien du manga
                manga_name = url_manga.split("/")[-1]                          # récupérer le nom du manga
                links_list.append(url_manga)                                   # Ajouter le lien à 'links_list'    
                manga_name_list.append(manga_name)                             # Ajouter le nom à 'manga_name_list'  
                # Action 2
                if "tome" in element_2.lower():                                # Si le manga contient des tomes
                    has_tome_list.append("yes")                                # Ajouter "yes" à 'has_tome_list'
                    result = re.search(r'Tome (\d+) -', element_2)             # Récupérer le dernier tome
                    last_tome = result.group(1)                                # récupérer uniquement le numéro du tome
                    last_tome_list.append(last_tome)                           # Ajouter le dernier tome à 'last_tome_list'
                else:
                    has_tome_list.append("no")                                 # Ajouter "no" à 'has_tome_list'
                    last_tome_list.append("None")                              # Ajouter "None" à 'last_tome_list'
                i += 1
            except:
                print(f"Pas de manga N°{i}, Fin Scrapping !")
                break
        print (len(manga_name_list)," mangas récupérés.\n")

        data_to_add = [{"name": name, "links": links, "has_tome": has_tome, "last_tome": last_tome} for name, links, has_tome, last_tome in zip(manga_name_list, links_list, has_tome_list, last_tome_list)]

        datas = pd.DataFrame(data_to_add)

        print(f"\nSauvegarde des datas ...")
        datas.to_csv(f'{script_repo}/datas/mangas.csv', index=False)

        print(f"\nSauvegarde terminée !\n")

    except:
        print(f"An Error occurred ! Please Debug | {script_repo}")



# Uncomment to debug
#if __name__ == "__main__":
    #Scrap_Titles()