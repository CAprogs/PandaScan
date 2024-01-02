import requests
import pandas as pd
from bs4 import BeautifulSoup


def Get_number_of_pages(soup, LOG):
    """Get the number of pages from mangamoins.

    Args:
        soup (BeautifulSoup): soup of the first page
        LOG (Any): the logger

    Returns:
        int/None: the number of pages if success, None if an error occured
    """
    try:
        select_element = soup.select_one('body > main > div.ContentGauche > div.bottom_pages > div')
        if select_element:
            pages_element = select_element.find_all("a")
            last_page = pages_element[-1].text
            return int(last_page)
        else:
            LOG.debug("No select_element")
            return None
    except Exception as e:
        LOG.debug(f"Error | {e}")
        return None


def Scrap_titles(PATH_TO_MANGAMOINS, LOG):
    """Scrap mangas titles from mangamoins.

    Args:
        PATH_TO_MANGAMOINS (str): path to mangamoins directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    manga_name_list = []
    filters = [".", ":"]
    page = 1

    while True:
        url = f"https://mangamoins.shaeishu.co/?p={page}"

        try:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            if page == 1:
                last_page = Get_number_of_pages(soup, LOG)
                if last_page is None:
                    LOG.debug("Error : No page element found")
                    return "failed"
            elif page > last_page:
                LOG.debug(f"Last page : {url}")
                break
            select_element = soup.select_one('body > main > div.ContentGauche > div.LastSorties')

            if select_element:
                mangas = select_element.find_all("div", class_="sortie")
                if mangas == []:
                    LOG.debug(f"No manga added | {url}")
                    break
                for manga in mangas:
                    title_element = manga.find("p")
                    manga_name = title_element.next.lower().replace(" ", "-")
                    for filter in filters:
                        if filter in manga_name:
                            manga_name = manga_name.replace(filter, "")
                    if manga_name not in manga_name_list:
                        manga_name_list.append(manga_name)
                        LOG.debug(f"{manga_name} added")
                page += 1
            else:
                LOG.debug(f"No select_element | {url}")
                return "failed"

        except Exception as e:
            LOG.debug(f"Error | {e}")
            return "failed"

    if manga_name_list == []:
        return "failed"

    LOG.info(f"{len(manga_name_list)} mangas fetched.")

    datas = pd.DataFrame(manga_name_list, columns=["NomManga"])
    datas.to_csv(f'{PATH_TO_MANGAMOINS}/datas/mangas.csv', index=False)
    return "success"
