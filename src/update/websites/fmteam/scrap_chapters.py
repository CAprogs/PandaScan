import pandas as pd
import yaml
import re
import time
from selenium.webdriver.common.by import By


def Scrap_chapters(DRIVER, PATH_TO_FMTEAM, LOG):
    """Scrap the mangas chapters from fmteam.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_FMTEAM (str): path to fmteam directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    try:
        datas = pd.read_csv(f'{PATH_TO_FMTEAM}/datas/mangas.csv')
    except Exception as e:
        return LOG.debug(f"Error : {e}")
    manga_chapters_dict = {}
    chapters_and_links = []
    failed_mangas = []
    columns = ["NomSite", "NomManga", "Chapitres", "ChapterLink"]

    pattern = r'/ch/(\d+)/sub/(\d+)'

    for index, manga_name in enumerate(datas['NomManga']):
        url = datas['links'][index]
        DRIVER.get(url)

        time.sleep(2)

        i = 2
        LOG.debug(f"Manga : {manga_name}")
        manga_chapters_dict[manga_name] = []

        while True:
            balise = str(f'//*[@id="comic"]/div[3]/div[2]/div[{i}]/div[1]/a[1]')
            try:
                element = DRIVER.find_element(By.XPATH, balise)
                download_link = element.get_attribute('href')
                if "sub" in download_link:
                    matches = re.search(pattern, download_link)
                    ch_number = matches.group(1)
                    sub_number = matches.group(2)
                    chapter_number = ch_number + "." + sub_number
                else:
                    chapter_number = download_link.split("/")[-1]

                chapter = "chapitre " + chapter_number
                manga_chapters_dict[manga_name].append(chapter)
                chapters_and_links.append(["fmteam", manga_name, chapter, download_link])
                LOG.debug(f"{chapter} added | link : {download_link}")
                i += 1
            except Exception as e:
                LOG.debug(f"{len(manga_chapters_dict[manga_name])} chapters fetched")
                if manga_chapters_dict[manga_name] == []:
                    failed_mangas.append(manga_name)
                try:
                    int(chapter_number)
                    LOG.debug(f"Chapter N°{int(chapter_number) - 1} doesn't exist | {manga_name}\n {e}")
                    break
                except Exception as e:
                    LOG.debug(f"Chapter N°{int(ch_number) - 1} doesn't exist | {manga_name}\n {e}")
                    break

    if len(failed_mangas) == len(datas['NomManga']):
        LOG.debug("Error : All mangas failed ..")
        return "failed"
    elif failed_mangas != []:
        LOG.debug(f"\n{len(failed_mangas)} mangas failed ..\n")
        for manga in failed_mangas:
            LOG.debug(manga)

    links_dataframe = pd.DataFrame(chapters_and_links, columns=columns)
    links_dataframe.to_csv(f'{PATH_TO_FMTEAM}/datas/chapters_links.csv', index=False)
    yml_data = yaml.dump(manga_chapters_dict)

    with open(f'{PATH_TO_FMTEAM}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
    return "success"
