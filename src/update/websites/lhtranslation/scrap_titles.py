import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def Scrap_titles(DRIVER, PATH_TO_LHTRANSLATION, LOG):
    """Scrap the mangas titles from lhtranslation.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_LHTRANSLATION (str): path to lhtranslation's directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    links_list = []
    manga_name_list = []

    url = "https://lhtranslation.net/?s&post_type=wp-manga&m_orderby=alphabet"

    DRIVER.get(url)
    
    while True:
        try:
            load_more_element = DRIVER.find_element(By.XPATH, '//*[@id="navigation-ajax"]/div[1]')
            if load_more_element != [] and load_more_element.text == 'LOAD MORE':
                # Wait for the element to be clickable, scroll to it and click
                locator = (By.XPATH, '//*[@id="navigation-ajax"]/div[1]')
                load_more_element = WebDriverWait(DRIVER, 5).until(EC.element_to_be_clickable(locator))
                ActionChains(DRIVER).move_to_element(load_more_element).click().perform()
            else:
                break
        except Exception as e:
            LOG.debug(f"Error : {e}")
            return "failed"

    try:
        elements = DRIVER.find_elements(By.CLASS_NAME, 'post-title')
        if elements != []:
            for element in elements:
                link = element.find_element(By.TAG_NAME, 'a')
                href_value = link.get_attribute('href')
                manga_name = href_value.split("/")[-2]
                links_list.append(href_value)
                manga_name_list.append(manga_name)
                LOG.debug(f"{manga_name} added | {href_value}")
        else:
            LOG.debug(f"No elements found | {url} | lhtranslation")

    except Exception as e:
        LOG.debug(f"Error | {e}")
        return "failed"

    if manga_name_list == []:
        return "failed"

    LOG.info(f"{len(manga_name_list)} mangas fetched.")

    data_to_add = [{"NomManga": name, "links": links} for name, links in zip(manga_name_list, links_list)]
    datas = pd.DataFrame(data_to_add)
    datas.to_csv(f'{PATH_TO_LHTRANSLATION}/datas/mangas.csv', index=False)
    return "success"
