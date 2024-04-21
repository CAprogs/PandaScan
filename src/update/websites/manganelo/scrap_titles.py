import requests
import pandas as pd
from bs4 import BeautifulSoup


def Scrap_titles(PATH_TO_MANGANELO: str, LOG):
    """Scrap mangas titles from manganelo.

    Args:
        PATH_TO_MANGANELO (str): path to manganelo directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    links_list = []
    manga_name_list = []
    filters = [".", ",", ";", ":", "!", "?", "'", "(", ")", "～", "*", "&", "=", "«", "»", "·", "~", "，", "'", "\"", " -", "「", " –", "’", "」"]
    page = 1

    while True:
        url = f"https://ww7.manganelo.tv/genre?page={page}"

        try:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            select_element = soup.select_one('body > div.body-site > div.container.container-main > div.panel-content-genres')
            if select_element is None:
                LOG.debug(f"No element found here | {url}")
                break

            mangas = select_element.find_all("div", class_="content-genres-item")
            if mangas == []:
                LOG.debug(f"No manga added | {url}")
                break
            for manga in mangas:
                title_element = manga.find("div", class_="genres-item-info")
                manga_name = title_element.find("a").get("title").lower()
                for filter in filters:
                    if filter in manga_name:
                        manga_name = manga_name.replace(filter, "")
                link = "https://ww7.manganelo.tv" + title_element.find("a").get("href")
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
    datas.to_csv(f'{PATH_TO_MANGANELO}/datas/mangas.csv', index=False)
    return "success"
