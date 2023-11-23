import pandas as pd
import yaml
import re
from selenium.webdriver.common.by import By


def Scrap_chapters(DRIVER, PATH_TO_FMTEAM, LOG):
    """Scrap the mangas chapters from fmteam.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_FMTEAM (str): path to fmteam directory
        LOG (Any): logger d'affichage
    """

    datas = pd.read_csv(f'{PATH_TO_FMTEAM}/datas/mangas.csv')
    manga_chapters_dict = {}

    pattern = r'/ch/(\d+)/sub/(\d+)'

    for index, manga_name in enumerate(datas['name']):
        url = datas['links'][index]
        DRIVER.get(url)

        DRIVER.implicitly_wait(1)

        i = 2      # dernier chapitre de la page de téléchargement
        LOG.debug(f"Manga : {manga_name}")
        manga_chapters_dict[manga_name] = []

        while True:
            balise = str(f'//*[@id="comic"]/div[3]/div[2]/div[{i}]/div[1]/a[1]')
            try:
                element = DRIVER.find_element(By.XPATH, balise)
                url_chapter_download = element.get_attribute('href')
                if "sub" in url_chapter_download:
                    matches = re.search(pattern, url_chapter_download)
                    if matches:
                        ch_number = matches.group(1)
                        sub_number = matches.group(2)
                        chapter_number = ch_number + "." + sub_number
                    else:
                        LOG.debug("ERREUR, AUCUN MATCH")
                else:
                    chapter_number = url_chapter_download.split("/")[-1]

                chapter = "chapitre " + chapter_number
                manga_chapters_dict[manga_name].append(chapter)
                LOG.debug(f"{chapter} récupéré ")
                i += 1
            except Exception as e:
                try:
                    int(chapter_number)
                    LOG.debug(f"Chapitre N°{int(chapter_number)-1} INEXISTANT | {manga_name}\n Error : {e}")
                    break
                except Exception as e:
                    LOG.debug(f"Chapitre N°{int(ch_number)-1} INEXISTANT | {manga_name}\n Error : {e}")
                    break

    yml_data = yaml.dump(manga_chapters_dict)

    with open(f'{PATH_TO_FMTEAM}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
