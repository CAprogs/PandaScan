import requests
import pandas as pd
import yaml
from bs4 import BeautifulSoup


def Scrap_chapters(PATH_TO_LELSCANS, LOG):
    """Scrap the mangas chapters from lelscans.

    Args:
        PATH_TO_LELSCANS (str): path to lelscans directory ( update )
        LOG (Any): logger d'affichage
    """

    datas = pd.read_csv(f'{PATH_TO_LELSCANS}/datas/mangas.csv')  # Accès mangas et liens
    manga_chapters_dict = {}  # création du dictionnaire qui contiendra les chapitres respectifs de chaque manga

    LOG.debug("Debut Scrapping ...")
    for index, manga_name in enumerate(datas['name']):
        url = datas['links'][index]
        try:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            select_element = soup.select_one('#header-image > h2 > form > select:nth-child(1)')

            LOG.debug(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = []  # Crée une clé de dictionnaire vide , avec le nom du manga qu'on explore.

            if select_element and select_element.name == "select":
                for option in select_element.find_all("option"):
                    desired_part = option["value"].split("/")[-1]  # on récupère uniquement le numéro de chapitre
                    chapter = "chapitre " + desired_part
                    manga_chapters_dict[manga_name].append(chapter)  # Ajouter le chapitre à 'manga_chapters_dict' avec sa clé correspondante
                    LOG.debug(f"{chapter} ajouté")

            else:
                LOG.debug(f"Erreur, aucun chapitre trouvé | {manga_name}")

        except Exception as e:
            LOG.debug(f"Error : {e} | {PATH_TO_LELSCANS}")
            break

    # Convertir le dictionnaire en document YAML
    yml_data = yaml.dump(manga_chapters_dict)

    with open(f'{PATH_TO_LELSCANS}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)

    LOG.debug("Fin Scrapping.")
