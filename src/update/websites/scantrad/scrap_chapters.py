import pandas as pd
import re
import yaml
import time
from selenium.webdriver.common.by import By


def Scrap_chapters(DRIVER, PATH_TO_SCANTRAD, LOG):
    """Scrap the mangas chapters from scantrad.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_SCANTRAD (str): path to scantrad directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    try:
        datas = pd.read_csv(f'{PATH_TO_SCANTRAD}/datas/mangas.csv')
    except Exception as e:
        LOG.debug(f"Error : {e}")
        return "failed"
    manga_chapters_dict = {}
    chapters_and_links = []
    failed_mangas = []
    last_manga_index = len(datas['NomManga']) - 1
    columns = ["NomSite", "NomManga", "Chapitres", "ChapterLink"]

    for index, manga_name in enumerate(datas['NomManga']):
        url = datas['links'][index]

        try:
            DRIVER.get(url)
            LOG.debug(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = []
            time.sleep(0.5)
            elements = DRIVER.find_elements(By.CLASS_NAME, 'wp-manga-chapter  ')

            for element in elements:
                # extract the chapter and his link
                link = element.find_element(By.TAG_NAME, 'a')
                chapter_link = link.get_attribute('href')
                result = re.search(rf'/{manga_name}/([^/]+)/', chapter_link)
                chapter = result.group(1).replace('-', ' ')
                manga_chapters_dict[manga_name].append(chapter)
                chapters_and_links.append(["scantrad", manga_name, chapter, chapter_link])
                LOG.debug(f"{chapter} added | {chapter_link}")

            LOG.debug(f"{len(manga_chapters_dict[manga_name])} chapters fetched.")

        except Exception as e:
            failed_mangas.append(manga_name)
            LOG.debug(f"Error : {e} | {url} | scantrad")
            if index != last_manga_index:
                continue

    if len(failed_mangas) == len(datas['NomManga']):
        LOG.debug("Error : All mangas failed ..")
        return "failed"
    elif failed_mangas != []:
        LOG.debug(f"\n{len(failed_mangas)} mangas failed ..\n")
        for manga in failed_mangas:
            LOG.debug(manga)

    links_dataframe = pd.DataFrame(chapters_and_links, columns=columns)
    links_dataframe.to_csv(f'{PATH_TO_SCANTRAD}/datas/chapters_links.csv', index=False)

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_SCANTRAD}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
    return "success"
