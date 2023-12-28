import pandas as pd
import re
from selenium.webdriver.common.by import By


def Scrap_titles(DRIVER, PATH_TO_SCANTRAD, LOG):
    """Scrap the mangas titles from scantrad.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_SCANTRAD (str): path to scantrad directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    page = 1
    a = ""
    links_list = []
    manga_name_list = []

    while True:

        if page == 1:
            page_url = f"https://scantrad-vf.me/manga/{a}?m_orderby=alphabet"
        else:
            page_url = f"https://scantrad-vf.me/manga/page/{page}/?m_orderby=alphabet"

        try:
            DRIVER.get(page_url)

            DRIVER.implicitly_wait(1)

            LOG.debug(f"Page {page} :")

            elements = DRIVER.find_elements(By.CLASS_NAME, 'h5')
            if elements != []:
                for element in elements:
                    link = element.find_element(By.TAG_NAME, 'a')
                    href_value = link.get_attribute('href')
                    result = re.search(r'/manga/([^/]+)/', href_value)
                    if result:
                        manga_name = result.group(1)
                        links_list.append(href_value)
                        manga_name_list.append(manga_name)
                        LOG.debug(f"{manga_name} added | {href_value}")
                    else:
                        LOG.debug(f"No value found for {href_value}. Page N°{page} | scantrad")
                page += 1
            else:
                break

        except Exception as e:
            LOG.debug(f"Error : {e} | Page N°{page} | scantrad")
            return "failed"

    if manga_name_list == []:
        return "failed"

    LOG.info(f"{len(manga_name_list)} mangas fetched.")

    data_to_add = [{"NomManga": name, "links": links} for name, links in zip(manga_name_list, links_list)]
    datas = pd.DataFrame(data_to_add)
    datas.to_csv(f'{PATH_TO_SCANTRAD}/datas/mangas.csv', index=False)
    return "success"
