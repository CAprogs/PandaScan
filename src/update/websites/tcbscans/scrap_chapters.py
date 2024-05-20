import requests
import pandas as pd
import yaml
from bs4 import BeautifulSoup


def Scrap_chapters(PATH_TO_TCBSCANS: str, LOG):
    """Scrap the mangas chapters from tcbscans.

    Args:
        PATH_TO_TCBSCANS (str): path to tcbscans directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    try:
        datas = pd.read_csv(f'{PATH_TO_TCBSCANS}/datas/mangas.csv')
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
            select_element = soup_1.select_one('body > main > div.overflow-hidden > div > div > div.col-span-2')

            LOG.debug(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = set()
            chapters_elements = select_element.find_all("a")

            for element in chapters_elements:
                chapter_title = [element.text for element in element.contents if "text-lg font-bold" in str(element)]
                # extract the chapter and his link
                chapter = "chapter " + chapter_title[0].split("Chapter", 1)[1].strip()
                chapter_link = 'https://tcbscans.com' + element['href']
                manga_chapters_dict[manga_name].add(chapter)
                chapters_and_links.append(["tcbscans", manga_name, chapter, chapter_link])
                LOG.debug(f"{chapter} added | link : {chapter_link}")

            datas.loc[index, 'n_chapter'] = len(manga_chapters_dict[manga_name])
            LOG.debug(f"{len(manga_chapters_dict[manga_name])} chapters fetched.")
            manga_chapters_dict[manga_name] = list(manga_chapters_dict[manga_name])
            manga_chapters_dict[manga_name].sort(key=lambda x: float(x.split()[1]), reverse=True)

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
    links_dataframe.to_csv(f'{PATH_TO_TCBSCANS}/datas/chapters_links.csv', index=False)

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_TCBSCANS}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)

    datas.to_csv(f'{PATH_TO_TCBSCANS}/datas/mangas.csv', index=False)
    return "success"
