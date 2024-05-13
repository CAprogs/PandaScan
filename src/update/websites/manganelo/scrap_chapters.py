import requests
import pandas as pd
import yaml
from bs4 import BeautifulSoup


def Scrap_chapters(PATH_TO_MANGANELO: str, LOG):
    """Scrap the mangas chapters from manganelo.

    Args:
        PATH_TO_MANGANELO (str): path to manganelo directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    try:
        datas = pd.read_csv(f'{PATH_TO_MANGANELO}/datas/mangas.csv')
    except Exception as e:
        LOG.debug(f"Error : {e}")
        return "failed"
    manga_chapters_dict = {}
    chapters_and_links = []
    failed_mangas = []
    last_manga_index = len(datas['MangaName']) - 1
    columns = ["Website", "MangaName", "Chapter", "ChapterLink"]

    for index, manga_name in enumerate(datas['MangaName']):
        url = datas['MangaLink'][index]

        try:
            response = requests.get(url)
            html_content = response.text
            soup_1 = BeautifulSoup(html_content, "html.parser")
            select_element = soup_1.select_one('body > div.body-site > div.container.container-main > div.container-main-left > div.panel-story-chapter-list > ul')

            LOG.debug(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = set()
            li_elements = select_element.find_all('li', class_="a-h")

            for li_element in li_elements:
                soup_2 = BeautifulSoup(str(li_element), 'html.parser')
                a_element = soup_2.find('a')
                # extract the chapter and his link
                chapter_link = "https://ww7.manganelo.tv" + a_element['href']
                chapter = chapter_link.split("/")[-1].replace("-", " ")
                manga_chapters_dict[manga_name].add(chapter)
                chapters_and_links.append(["manganelo", manga_name, chapter, chapter_link])
                LOG.debug(f"{chapter} added | link : {chapter_link}")

            datas.loc[index, 'n_chapter'] = len(manga_chapters_dict[manga_name])
            LOG.debug(f"{len(manga_chapters_dict[manga_name])} chapters fetched.")

        except Exception as e:
            failed_mangas.append(manga_name)
            LOG.debug(f"Error : {e} | {url}")
            if index != last_manga_index:
                continue

    if len(failed_mangas) == len(datas['MangaName']):
        LOG.debug("Error : All mangas failed ..")
        return "failed"
    elif failed_mangas != []:
        LOG.debug(f"\n{len(failed_mangas)} mangas failed ..\n")
        for manga in failed_mangas:
            LOG.debug(manga)

    links_dataframe = pd.DataFrame(chapters_and_links, columns=columns)
    links_dataframe.to_csv(f'{PATH_TO_MANGANELO}/datas/chapters_links.csv', index=False)

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_MANGANELO}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)

    datas.to_csv(f'{PATH_TO_MANGANELO}/datas/mangas.csv', index=False)
    return "success"
