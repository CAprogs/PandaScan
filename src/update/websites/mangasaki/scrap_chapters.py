import pandas as pd
import yaml
from selenium.webdriver.common.by import By


def Scrap_chapters(DRIVER, PATH_TO_MANGASAKI, LOG):
    """Scrap the mangas chapters from mangasaki.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_MANGASAKI (str): path to mangasaki directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    try:
        datas = pd.read_csv(f'{PATH_TO_MANGASAKI}/datas/mangas.csv')
    except Exception as e:
        LOG.debug(f"Error : {e}")
        return "failed"
    manga_chapters_dict = {}
    chapters_and_links = []
    failed_mangas = []
    last_manga_index = len(datas['NomManga'])-1
    columns = ["NomSite", "NomManga", "Chapitres", "ChapterLink"]

    for index, manga_name in enumerate(datas['NomManga']):
        url = datas['links'][index]
        i = 0
        previous_chapter_number = 0
        
        LOG.info(f"Manga : {manga_name}")
        manga_chapters_dict[manga_name] = []

        while True:
            try:
                DRIVER.get(url + f"?page={i}")

                if i == 0:
                    ul_elements = DRIVER.find_elements(By.TAG_NAME, 'ul')[16]
                    last_page_element = ul_elements.find_elements(By.TAG_NAME, 'li')[-1].find_element(By.TAG_NAME, 'a')
                    if last_page_element and last_page_element.text == "last »":
                        try:
                            last_page = int(last_page_element.get_attribute('href').split("=")[-1])
                        except Exception as e:
                            LOG.debug(f"No last_page_element | {url}")
                            last_page_element = None
                    else:
                        LOG.debug(f"No last_page_element | {url}")
                        last_page_element = None
                elif i > last_page:
                    break
                
                select_element = DRIVER.find_element(By.TAG_NAME, 'tbody')
                options = select_element.find_elements(By.TAG_NAME, 'tr')

                for option in options:
                    # extract the chapter and his link
                    link_element = option.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'a')
                    chapter_link = link_element.get_attribute('href')
                    pattern = f"https://www.mangasaki.org/chapter/{manga_name}-"
                    if pattern not in chapter_link:
                        continue
                    else:
                        split_link = chapter_link.replace(pattern, "").split("-")
                    try:
                        number_1 = int(split_link[0])
                    except Exception as e:
                        continue
                    try:
                        number_2 = int(split_link[1])
                        chapter_number = float(str(number_1) + "." + str(number_2))
                    except Exception as e:
                        if number_1:
                            chapter_number = number_1
                        else:
                            LOG.debug(f"No chapter added. | {e}")
                            continue

                    if i == 0 and manga_chapters_dict[manga_name] == []:
                        previous_chapter_number = chapter_number
                    else:
                        if float(chapter_number) > float(previous_chapter_number):
                            try:
                                chapter_number = float(link_element.text.replace("-", ".").split(" ")[-1])
                            except Exception as e:
                                LOG.debug(f"{e} | {chapter_number}")
                                continue
                        elif float(chapter_number) == float(previous_chapter_number):
                            LOG.debug(f"The chapter number is the same as the previous one. | {chapter_number}")
                            continue
                        
                        previous_chapter_number = chapter_number

                    chapter = "chapter " + str(chapter_number)
                    manga_chapters_dict[manga_name].append(chapter)
                    chapters_and_links.append(["mangasaki", manga_name, chapter, chapter_link])
                    LOG.debug(f"{chapter} added | link : {chapter_link}")

                if last_page_element == None:
                    break
                i += 1

            except Exception as e:
                failed_mangas.append(manga_name)
                LOG.debug(f"Error : {e} | {url}")
                if index != last_manga_index:
                    break

        LOG.info(f"{len(manga_chapters_dict[manga_name])} chapters fetched")

    if len(failed_mangas) == len(datas['NomManga']):
        LOG.debug("Error : All mangas failed ..")
        return "failed"
    elif failed_mangas != []:
        LOG.debug(f"\n{len(failed_mangas)} mangas failed ..\n")
        for manga in failed_mangas:
            LOG.debug(manga)

    links_dataframe = pd.DataFrame(chapters_and_links, columns=columns)
    links_dataframe.to_csv(f'{PATH_TO_MANGASAKI}/datas/chapters_links.csv', index=False)

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_MANGASAKI}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
    return "success"
