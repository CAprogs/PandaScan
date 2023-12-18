import requests
import pandas as pd
import yaml
from bs4 import BeautifulSoup


def Scrap_chapters(PATH_TO_LELSCANS, LOG):
    """Scrap the mangas chapters from lelscans.

    Args:
        PATH_TO_LELSCANS (str): path to lelscans directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    try:
        datas = pd.read_csv(f'{PATH_TO_LELSCANS}/datas/mangas.csv')
    except Exception as e:
        return LOG.debug(f"Error : {e}")
    manga_chapters_dict = {}
    chapters_and_links = []
    failed_mangas = []
    last_manga_index = len(datas['NomManga']) - 1
    columns = ["NomSite", "NomManga", "Chapitres", "ChapterLink"]

    for index, manga_name in enumerate(datas['NomManga']):
        url = datas['links'][index]

        try:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            select_element = soup.select_one('#header-image > h2 > form > select:nth-child(1)')

            LOG.debug(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = []

            for option in select_element.find_all("option"):
                # extract the chapter and his link
                chapter_link = option["value"]
                chapter = "chapitre " + chapter_link.split("/")[-1]
                manga_chapters_dict[manga_name].append(chapter)
                chapters_and_links.append(["lelscans", manga_name, chapter, chapter_link])
                LOG.debug(f"{chapter} added | link : {chapter_link}")

            LOG.debug(f"{len(manga_chapters_dict[manga_name])} chapters fetched")

        except Exception as e:
            failed_mangas.append(manga_name)
            LOG.debug(f"Error : {e} | {url}")
            if index != last_manga_index:
                continue

    if len(failed_mangas) == len(datas['NomManga']):
        LOG.debug("Error : All mangas failed ..")
        return "failed"
    elif failed_mangas != []:
        LOG.debug(f"\n{len(failed_mangas)} mangas failed ..\n")
        for manga in failed_mangas:
            LOG.debug(manga)

    links_dataframe = pd.DataFrame(chapters_and_links, columns=columns)
    links_dataframe.to_csv(f'{PATH_TO_LELSCANS}/datas/chapters_links.csv', index=False)

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_LELSCANS}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
    return "success"
