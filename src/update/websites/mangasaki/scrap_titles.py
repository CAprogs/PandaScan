import pandas as pd
from selenium.webdriver.common.by import By
from ..mangasaki.utils import get_manga_name


def Scrap_titles(DRIVER, PATH_TO_MANGASAKI: str, LOG):
    """Scrap mangas titles from mangasaki.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_MANGASAKI (str): path to mangasaki directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    links_list = []
    manga_name_list = []
    page = 0

    while True:
        url = f"https://www.mangasaki.org/directory?page={page}"

        try:
            DRIVER.get(url)
            select_element = DRIVER.find_element(By.TAG_NAME, 'tbody')

            if page == 0:
                last_page_element = DRIVER.find_element(By.XPATH, '//*[@id="box"]/div[1]/ul/li[12]/a')
                if last_page_element:
                    last_page = int(last_page_element.get_attribute('href').split("=")[-1])
                else:
                    LOG.debug(f"No last_page_element | {url}")
                    return "failed"
            elif page > last_page:
                break

            if select_element:
                mangas = select_element.find_elements(By.TAG_NAME, 'tr')
                if mangas == []:
                    LOG.debug(f"No manga added | {url}")
                    break
                for manga in mangas:
                    link_element = manga.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'a')
                    href_value = link_element.get_attribute('href')
                    manga_name = href_value.split("/")[-1]

                    manga_name = get_manga_name(manga_name)

                    links_list.append(href_value)
                    manga_name_list.append(manga_name)
                    LOG.debug(f"{manga_name} added | {href_value}")
            else:
                LOG.debug(f"No select_element | {url}")
                break
            page += 1

        except Exception as e:
            LOG.debug(f"Error | {e}")
            return "failed"

    if manga_name_list == []:
        return "failed"

    LOG.info(f"{len(manga_name_list)} mangas fetched.")

    data_to_add = [{"MangaName": name, "MangaLink": link} for name, link in zip(manga_name_list, links_list)]
    datas = pd.DataFrame(data_to_add)
    datas['n_chapter'] = 0
    datas.to_csv(f'{PATH_TO_MANGASAKI}/datas/mangas.csv', index=False)
    return "success"
