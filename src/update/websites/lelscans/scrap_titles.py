import requests
import pandas as pd
from bs4 import BeautifulSoup


def Scrap_titles(PATH_TO_LELSCANS, LOG):
    """Scrap mangas titles from lelscans.

    Args:
        PATH_TO_LELSCANS (str): path to lelscans directory (update)
        LOG (Any): the logger
    """

    links_list = []
    manga_name_list = []

    url = "https://lelscans.net/scan-hunter-x-hunter/400/1"

    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        select_element = soup.select_one('#header-image > h2 > form > select:nth-child(2)')

        if select_element and select_element.name == "select":
            for option in select_element.find_all("option"):
                url_manga = option["value"]
                links_list.append(url_manga)

                desired_part = url_manga.split("/")[-1]
                if "lecture-ligne-" in desired_part:
                    manga_name = desired_part.replace("lecture-ligne-", "").replace(".php", "")
                    LOG.debug(f"{manga_name} added")
                    manga_name_list.append(manga_name)
                else:
                    manga_name = desired_part.replace("lecture-en-ligne-", "").replace(".php", "")
                    LOG.debug(f"{manga_name} added")
                    manga_name_list.append(manga_name)

            LOG.info(f"{len(manga_name_list)} mangas fetched")
            if len(manga_name_list) == 0:
                return "failed"

            data_to_add = [{"NomManga": name, "links": links} for name, links in zip(manga_name_list, links_list)]
            datas = pd.DataFrame(data_to_add)
            datas.to_csv(f'{PATH_TO_LELSCANS}/datas/mangas.csv', index=False)
            return "success"

        else:
            LOG.debug("Error: no manga added | Lelscans")
            return "failed"

    except Exception as e:
        LOG.debug(f"Error : {e} | Lelscans")
        return "failed"
