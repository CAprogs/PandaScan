import pandas as pd
from selenium.webdriver.common.by import By


def Scrap_titles(DRIVER, PATH_TO_FMTEAM, LOG):
    """Scrap the mangas titles from fmteam.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_FMTEAM (str): path to fmteam directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    manga_name_list = []
    links_list = []

    url = "https://fmteam.fr/comics"

    try:
        DRIVER.get(url)

        DRIVER.implicitly_wait(5)

        i = 1
        while True:
            balise = str(f'//*[@id="app"]/main/div/div/div[2]/div[{i}]/div[2]/h5/a')

            try:
                element = DRIVER.find_element(By.XPATH, balise)
                url_manga = element.get_attribute('href')
                manga_name = url_manga.split("/")[-1]
                LOG.debug(f"{manga_name} added")
                links_list.append(url_manga)
                manga_name_list.append(manga_name)
                i += 1
            except Exception as e:
                LOG.debug(f"No manga N°{i}\nError : {e}")
                break

        if manga_name_list == []:
            return "failed"

        LOG.info(f"{len(manga_name_list)} mangas fetched.")

        data_to_add = [{"NomManga": name, "links": links} for name, links in zip(manga_name_list, links_list)]
        datas = pd.DataFrame(data_to_add)
        datas.to_csv(f'{PATH_TO_FMTEAM}/datas/mangas.csv', index=False)
        return "success"

    except Exception as e:
        LOG.debug(f"Error : {e} | Fmteam")
        return "failed"
