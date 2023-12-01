import requests
import pandas as pd
import yaml
from bs4 import BeautifulSoup


def Scrap_chapters(PATH_TO_LELSCANS, LOG):
    """Scrap the mangas chapters from lelscans.

    Args:
        PATH_TO_LELSCANS (str): path to lelscans directory (update)
        LOG (Any): the logger
    """

    datas = pd.read_csv(f'{PATH_TO_LELSCANS}/datas/mangas.csv')
    manga_chapters_dict = {}

    for index, manga_name in enumerate(datas['NomManga']):
        url = datas['links'][index]
        try:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            select_element = soup.select_one('#header-image > h2 > form > select:nth-child(1)')

            LOG.debug(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = []

            if select_element and select_element.name == "select":
                for option in select_element.find_all("option"):
                    desired_part = option["value"].split("/")[-1]
                    chapter = "chapitre " + desired_part
                    manga_chapters_dict[manga_name].append(chapter)
                    LOG.debug(f"{chapter} added")
                LOG.debug(f"{len(manga_chapters_dict[manga_name])} chapters fetched")

            else:
                LOG.debug(f"Error, No chapter found | {manga_name}")

        except Exception as e:
            LOG.debug(f"Error : {e} | {PATH_TO_LELSCANS}")
            break

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_LELSCANS}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
