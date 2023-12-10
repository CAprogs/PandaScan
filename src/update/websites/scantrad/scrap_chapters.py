import pandas as pd
import re
import yaml
from selenium.webdriver.common.by import By


def Scrap_chapters(DRIVER, PATH_TO_SCANTRAD, LOG):
    """Scrap the mangas chapters from scantrad.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_SCANTRAD (str): path to scantrad directory (update)
        LOG (Any): the logger
    """

    datas = pd.read_csv(f'{PATH_TO_SCANTRAD}/datas/mangas.csv')
    manga_chapters_dict = {}

    for manga_name in datas['NomManga']:
        url_start = f'https://scantrad-vf.co/manga/{manga_name}/'

        try:
            DRIVER.get(url_start)
            LOG.debug(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = []

            DRIVER.implicitly_wait(2)

            elements = DRIVER.find_elements(By.CLASS_NAME, 'wp-manga-chapter  ')
            for element in elements:
                link = element.find_element(By.TAG_NAME, 'a')
                href_value = link.get_attribute('href')
                result = re.search(rf'/{manga_name}/([^/]+)/', href_value)
                if result:
                    chapter = result.group(1)
                    if chapter:
                        chapter_str = chapter.replace('-', ' ')
                        manga_chapters_dict[manga_name].append(chapter_str)
                        LOG.debug(f"{chapter_str} added")
                    else:
                        LOG.debug(f"No value found | {href_value} | scantrad")
                else:
                    LOG.debug(f"No value found. | {manga_name} | scantrad")
        except Exception as e:
            LOG.debug(f"Error : {e} | {manga_name}")

    datas = datas.reset_index(drop=True)
    yml_data = yaml.dump(manga_chapters_dict)
    datas.to_csv(f'{PATH_TO_SCANTRAD}/datas/mangas.csv', index=False)
    with open(f'{PATH_TO_SCANTRAD}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
