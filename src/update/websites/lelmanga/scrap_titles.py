import requests
import pandas as pd
from bs4 import BeautifulSoup


def Scrap_titles(PATH_TO_LELMANGA, LOG):
    """Scrap mangas titles from lelmanga.

    Args:
        PATH_TO_LELMANGA (str): path to lelmanga directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    links_list = []
    manga_name_list = []
    page = 1

    while True:
        url = f"https://www.lelmanga.com/manga?page={page}"

        try:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            select_element = soup.select_one('#content > div.wrapper > div.postbody > div.bixbox.seriesearch > div.mrgn > div.listupd')
            mangas = select_element.find_all("div", class_="bs")

            if mangas == []:
                LOG.debug(f"No manga added | {url}")
                break
            for manga in mangas:
                link = manga.find("a").get("href")
                manga_name = link.split("/")[-1]
                links_list.append(link)
                manga_name_list.append(manga_name)
                LOG.debug(f"{manga_name} added | {link}")
            page += 1

        except Exception as e:
            LOG.debug(f"Error : {e}")
            return "failed"

    if manga_name_list == []:
        return "failed"

    LOG.info(f"{len(manga_name_list)} mangas fetched.")

    data_to_add = [{"NomManga": name, "links": links} for name, links in zip(manga_name_list, links_list)]
    datas = pd.DataFrame(data_to_add)
    datas.to_csv(f'{PATH_TO_LELMANGA}/datas/mangas.csv', index=False)
    return "success"
