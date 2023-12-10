import pandas as pd
import re
from selenium.webdriver.common.by import By


def Scrap_titles(DRIVER, PATH_TO_SCANTRAD, LOG):
    """Scrap the mangas titles from scantrad.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_SCANTRAD (str): path to scantrad directory (update)
        LOG (Any): the logger
    """

    page = 1
    a = ""
    mangas_titles = []

    while True:

        if page == 1:
            page_url = f"https://scantrad-vf.co/manga/{a}?m_orderby=alphabet"
        else:
            page_url = f"https://scantrad-vf.co/manga/page/{page}/?m_orderby=alphabet"

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
                    mangas_titles.append({"NomManga": manga_name})
                    LOG.debug(f"{manga_name} added")
                else:
                    LOG.debug(f"No value found for {href_value}. Page N°{page} | scantrad")
            page += 1
        else:
            break

    LOG.info(f"{len(mangas_titles)} mangas fetched.")

    datas = pd.DataFrame(mangas_titles)
    datas.to_csv(f'{PATH_TO_SCANTRAD}/datas/mangas.csv', index=False)
