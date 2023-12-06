import pandas as pd
import re
from selenium.webdriver.common.by import By


def Scrap_titles(DRIVER, PATH_TO_FMTEAM, LOG):
    """Scrap the mangas titles from fmteam.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_FMTEAM (str): path to fmteam directory (update)
        LOG (Any): the logger
    """

    manga_name_list = []
    links_list = []
    has_tome_list = []
    last_tome_list = []

    url = "https://fmteam.fr/comics"

    try:
        DRIVER.get(url)

        DRIVER.implicitly_wait(2)

        i = 1
        while True:
            balise_1 = str(f'//*[@id="app"]/main/div/div/div[2]/div[{i}]/div[2]/h5/a')  # Balise du nom du manga
            balise_2 = str(f'//*[@id="app"]/main/div/div/div[2]/div[{i}]/ul/li[4]/a')   # Balise du nom du Tome ou Chapitre
            try:
                element_1 = DRIVER.find_element(By.XPATH, balise_1)            # récupérer l'élément de la balise 1
                element_2 = DRIVER.find_element(By.XPATH, balise_2).text       # récupérer l'élément de la balise 2
                # Step 1
                url_manga = element_1.get_attribute('href')
                manga_name = url_manga.split("/")[-1]
                LOG.debug(f"{manga_name} added")
                links_list.append(url_manga)
                manga_name_list.append(manga_name)
                # Step 2
                if "tome" in element_2.lower():
                    has_tome_list.append("yes")
                    result = re.search(r'Tome (\d+) -', element_2)             # Récupérer le dernier tome
                    last_tome = result.group(1)                                # récupérer uniquement le numéro du tome
                    last_tome_list.append(last_tome)
                else:
                    has_tome_list.append("no")
                    last_tome_list.append("None")
                i += 1
            except Exception as e:
                LOG.debug(f"No manga N°{i}\nError : {e} | Fmteam")
                break

        LOG.info(f"{len(manga_name_list)} mangas fetched.")

        data_to_add = [{"NomManga": name, "links": links, "has_tome": has_tome, "last_tome": last_tome} for name, links, has_tome, last_tome in zip(manga_name_list, links_list, has_tome_list, last_tome_list)]
        datas = pd.DataFrame(data_to_add)
        datas.to_csv(f'{PATH_TO_FMTEAM}/datas/mangas.csv', index=False)

    except Exception as e:
        LOG.debug(f"Error : {e} | Fmteam")
