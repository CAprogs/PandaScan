import pandas as pd
import re
from selenium.webdriver.common.by import By


def Scrap_titles(DRIVER, PATH_TO_SCANTRAD, LOG):
    """Scrap the mangas titles from scantrad.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_SCANTRAD (str): path to scantrad directory
        LOG (Any): logger d'affichage
    """

    starting_page = 1
    a = ""
    page = 1
    datas = pd.DataFrame(columns=["name"])  # on crée un dataframe d'une colonne
    new_list = []  # création d'une liste vide

    LOG.debug("Debut Scrapping ...")
    while True:

        if starting_page == 1:
            url_start = f"https://scantrad-vf.co/manga/{a}?m_orderby=alphabet"
        else:
            url_start = f"https://scantrad-vf.co/manga/page/{page}/?m_orderby=alphabet"

        # Accès à la page avec selenium
        DRIVER.get(url_start)

        LOG.debug(f"Page {starting_page} :")

        # on récupère tous les éléments correspondant à la classe 'h5'
        elements = DRIVER.find_elements(By.CLASS_NAME, 'h5')
        if elements != []:
            # parcourir la liste des éléments de la classe h5
            for element in elements:
                link = element.find_element(By.TAG_NAME, 'a')
                # récupérer la valeur de l'attribut "href" de l'élément <a>
                valeur_href = link.get_attribute('href')
                # utiliser une expression régulière pour extraire uniquement le nom du manga
                result = re.search(r'/manga/([^/]+)/', valeur_href)
                if result:
                    manga_name = result.group(1)
                    new_list.append({"name": manga_name})
                    LOG.debug(f"{manga_name} ajouté")
                else:
                    LOG.debug(f"Aucune valeur trouvée pour {valeur_href}. Page N°{starting_page} | scantrad titles scraping")
            starting_page += 1
            page += 1
        else:
            break

    LOG.debug(f"{len(new_list)} mangas récupérés.")
    
    # ajouter le contenu de 'new_list' au dataframe 'datas'
    datas = pd.concat([datas, pd.DataFrame(new_list)], ignore_index=True)
    datas.to_csv(f'{PATH_TO_SCANTRAD}/datas/mangas.csv', index=False)
    
    LOG.debug("Fin Scrapping")
