import requests
import pandas as pd
from bs4 import BeautifulSoup


def Scrap_titles(PATH_TO_ANIMESAMA, LOG):
    """Scrap mangas titles from mangascan.

    Args:
        PATH_TO_ANIMESAMA (str): path to mangascan directory ( update )
        LOG (Any): logger d'affichage
    """

    links_list = []
    manga_name_list = []

    page = 1

    while True:
        url = f"https://anime-sama.me/manga/?page={page}&status=&type=&order=title"

        try:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            select_element = soup.select_one('#content > div > div.postbody > div.bixbox.seriesearch > div.mrgn > div.listupd')

            if select_element:
                mangas = select_element.find_all("div", class_="bs")
                if mangas == []:
                    LOG.debug(f"\nNo manga added | {url}")
                    break
                for manga in mangas:
                    link = manga.find("a").get("href")
                    manga_name = link.split("/")[-2]
                    links_list.append(link)
                    manga_name_list.append(manga_name)
                    LOG.debug(f"{manga_name} added | {link}")
            else:
                LOG.debug(f"\nNo select_element | {url}")
                break

            page += 1

        except Exception as e:
            LOG.debug(f"Error | {e}")
            return

    LOG.debug(f"{len(manga_name_list)} mangas added")
    data_to_add = [{"name": name, "links": links} for name, links in zip(manga_name_list, links_list)]
    datas = pd.DataFrame(data_to_add)
    datas.to_csv(f'{PATH_TO_ANIMESAMA}/datas/mangas.csv', index=False)
