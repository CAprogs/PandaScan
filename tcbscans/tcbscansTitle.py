import requests
import pandas as pd
from bs4 import BeautifulSoup

PATH_TO_TCBSCANS = "/Users/charles-albert/Desktop/PandaScan/tests/tcbscans"

def Scrap_titles():
    """Scrap mangas titles from tcbscans.

    Args:
        PATH_TO_TCBSCANS (str): path to tcbscans directory (update)
        LOG (Any): the logger
    """

    links_list = []
    manga_name_list = []

    url = "https://tcbscans.com/projects"

    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        select_element = soup.select_one('body > main > div.overflow-hidden > div > div.grid.grid-cols-1.md\:grid-cols-2.gap-3')

        if select_element:
            mangas = select_element.find_all("div", class_="relative h-24 w-24 sm:mb-0 mb-3")
            if mangas == []:
                print(f"No manga added | {url}")
                return
            for manga in mangas:
                link = 'https://tcbscans.com' + manga.find("a").get("href")
                manga_name = link.split("/")[-1]
                links_list.append(link)
                manga_name_list.append(manga_name)
                print(f"{manga_name} added | {link}")
        else:
            print(f"No select_element | {url}")
            return

    except Exception as e:
        print(f"Error | {e}")
        return

    print(f"{len(manga_name_list)} mangas fetched.")

    data_to_add = [{"NomManga": name, "links": links} for name, links in zip(manga_name_list, links_list)]
    datas = pd.DataFrame(data_to_add)
    datas.to_csv(f'{PATH_TO_TCBSCANS}/mangas.csv', index=False)


Scrap_titles()