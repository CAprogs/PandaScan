import pandas as pd
import re
import yaml
from selenium.webdriver.common.by import By


def Scrap_chapters(DRIVER, PATH_TO_SCANTRAD, LOG):
    """Scrap the mangas chapters from scantrad.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_SCANTRAD (str): path to scantrad directory
        LOG (Any): logger d'affichage
    """

    datas = pd.read_csv(f'{PATH_TO_SCANTRAD}/datas/mangas.csv')
    manga_chapters_dict = {}

    LOG.debug("Debut Scrapping ...")

    for manga_name in datas['name']:
        url_start = f'https://scantrad-vf.co/manga/{manga_name}/'

        try:
            DRIVER.get(url_start)
            LOG.debug(f"Manga : {manga_name}")  # Indique dans quel manga nous sommes pour le scrapping des chapitres
            manga_chapters_dict[manga_name] = []  # Crée une clé de dictionnaire vide , avec le nom du manga qu'on explore.

            DRIVER.implicitly_wait(1)   # Attendre que la page soit complètement chargée

            # Récupérer tous les éléments correspondant à la classe 'wp-manga-chapter  '
            elements = DRIVER.find_elements(By.CLASS_NAME, 'wp-manga-chapter  ')
            # Parcourir tous les éléments de la classe 'wp-manga-chapter  ' ( les chapitres du manga dans lequel on se trouve )
            for element in elements:
                link = element.find_element(By.TAG_NAME, 'a')
                # Récupérer la valeur de l'attribut "href" de l'élément <a>
                valeur_href = link.get_attribute('href')
                # Utiliser une expression régulière pour extraire la valeur
                result = re.search(rf'/{manga_name}/([^/]+)/', valeur_href)  # On récupère le chapitre
                if result:
                    chapter = result.group(1)
                    if chapter:
                        chapter_str = chapter.replace('-', ' ')
                        manga_chapters_dict[manga_name].append(chapter_str)  # Ajouter le chapitre à 'manga_chapters_dict' avec sa clé correspondante
                        LOG.debug(f"{chapter_str} ajouté")
                    else:
                        LOG.debug(f"Aucune valeur trouvée | {valeur_href} | scantrad chapter scraping")
                else:
                    LOG.debug(f"Aucune valeur trouvée. | {manga_name} | scantrad chapter scraping")
        except Exception as e:
            LOG.debug(f"Error : {e} | {manga_name}")

    # Réinitialiser les index du dataframe
    datas = datas.reset_index(drop=True)
    # Convertir le dictionnaire en document YAML
    yml_data = yaml.dump(manga_chapters_dict)

    datas.to_csv(f'{PATH_TO_SCANTRAD}/datas/mangas.csv', index=False)

    with open(f'{PATH_TO_SCANTRAD}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)

    LOG.debug("Fin Scrapping")
