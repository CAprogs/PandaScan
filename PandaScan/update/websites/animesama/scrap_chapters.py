import requests
import pandas as pd
import yaml
from bs4 import BeautifulSoup


def Scrap_chapters(PATH_TO_ANIMESAMA, LOG):
    """Scrap the mangas chapters from lelscans.

    Args:
        PATH_TO_ANIMESAMA (str): path to lelscans directory ( update )
        LOG (Any): logger d'affichage
    """

    datas = pd.read_csv(f'{PATH_TO_ANIMESAMA}/datas/mangas.csv')
    manga_chapters_dict = {}
    chapters_and_links = []
    columns = ["NomSite", "NomManga", "Chapitres", "ChapterLink"]

    for index, manga_name in enumerate(datas['name']):

        url = datas['links'][index]

        try:
            response = requests.get(url)
            html_content = response.text
            soup_1 = BeautifulSoup(html_content, "html.parser")

            select_element = soup_1.select_one('#chapterlist')
            if not select_element:
                LOG.debug(f"Error : No chapters found | {url}")
                exit()

            LOG.debug(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = []

            options = select_element.find("ul").contents

            for option in options:
                soup_2 = BeautifulSoup(str(option), 'html.parser')
                li_element = soup_2.find('li', {'data-num': True})
                a_element = li_element.find('a')
                # extract the chapter and his link
                chapter = "chapitre " + li_element['data-num']
                chapter_link = a_element['href']

                manga_chapters_dict[manga_name].append(chapter)
                chapters_and_links.append(["animesama", manga_name, chapter, chapter_link])
                LOG.debug(f"{chapter} added | link : {chapter_link}")

            LOG.debug(f"\n{len(manga_chapters_dict[manga_name])} chapters added")

        except Exception as e:
            LOG.debug(f"Error : {e} | animesama chapters scraping | {url}")
            return

    links_dataframe = pd.DataFrame(chapters_and_links, columns=columns)
    links_dataframe.to_csv(f'{PATH_TO_ANIMESAMA}/datas/chapters_links.csv', index=False)

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_ANIMESAMA}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
