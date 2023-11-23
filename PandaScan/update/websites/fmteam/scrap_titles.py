import pandas as pd
import re
from selenium.webdriver.common.by import By


def Scrap_titles(DRIVER, PATH_TO_FMTEAM, LOG):
    """Scrap the mangas titles from fmteam.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_FMTEAM (str): path to fmteam directory
        LOG (Any): logger d'affichage
    """

    manga_name_list = []
    links_list = []
    has_tome_list = []
    last_tome_list = []

    url = "https://fmteam.fr/comics"

    try:
        DRIVER.get(url)

        DRIVER.implicitly_wait(1)

        i = 1       # correspond au 1 er manga de la page
        while True:
            balise_1 = str(f'//*[@id="app"]/main/div/div/div[2]/div[{i}]/div[2]/h5/a')  # Balise du nom du manga
            balise_2 = str(f'//*[@id="app"]/main/div/div/div[2]/div[{i}]/ul/li[4]/a')   # Balise du nom du Tome ou Chapitre
            try:
                element_1 = DRIVER.find_element(By.XPATH, balise_1)            # récupérer l'élément de la balise 1
                element_2 = DRIVER.find_element(By.XPATH, balise_2).text       # récupérer l'élément de la balise 2
                # Action 1
                url_manga = element_1.get_attribute('href')                    # récupérer le lien du manga
                manga_name = url_manga.split("/")[-1]                          # récupérer le nom du manga
                LOG.debug(f"{manga_name} ajouté")
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
            except Exception as e:
                LOG.debug(f"Pas de manga N°{i}\nError : {e}")
                break
        LOG.debug(f"{len(manga_name_list)} mangas récupérés.")

        data_to_add = [{"name": name, "links": links, "has_tome": has_tome, "last_tome": last_tome} for name, links, has_tome, last_tome in zip(manga_name_list, links_list, has_tome_list, last_tome_list)]
        datas = pd.DataFrame(data_to_add)
        datas.to_csv(f'{PATH_TO_FMTEAM}/datas/mangas.csv', index=False)

    except Exception as e:
        LOG.debug(f"Error : {e} | Fmteam titles scrapping")
