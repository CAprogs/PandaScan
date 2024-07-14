import requests
import pandas as pd
import yaml
from bs4 import BeautifulSoup
from ..mangamoins.scrap_titles import Get_number_of_pages


def Scrap_chapters(PATH_TO_MANGAMOINS: str, LOG):
    """Scrap the mangas chapters from mangamoins.

    Args:
        PATH_TO_MANGAMOINS (str): path to mangamoins directory (update)
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    try:
        datas = pd.read_csv(f'{PATH_TO_MANGAMOINS}/datas/mangas.csv')
    except Exception as e:
        LOG.debug(f"Error : {e}")
        return "failed"
    manga_chapters_dict = {}
    chapters_and_links = []
    filter = [".", ":"]
    columns = ["Website", "MangaName", "Chapter", "ChapterLink"]
    page = 1

    for manga in datas['MangaName']:
        manga_chapters_dict[manga] = set()

    while True:
        url = f"https://mangamoins.shaeishu.co/?p={page}"

        try:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            if page == 1:
                last_page = Get_number_of_pages(soup, LOG)
                if last_page is None:
                    LOG.debug("Error : No last page found")
                    return
            elif page > last_page:
                LOG.debug(f"End of scraping | {url}")
                break

            select_element = soup.select_one('body > main > div.ContentGauche > div.LastSorties')
            if not select_element:
                LOG.debug(f"Error : No chapters found | {url} | mangamoins")
                return

            manga_elements = select_element.find_all("div", class_="sortie")
            if manga_elements == []:
                LOG.debug(f"No manga added | {url}")
                break
            for manga in manga_elements:
                title_element = manga.find("p")
                manga_name = title_element.next.lower().replace(" ", "-")
                for char in filter:
                    if char in manga_name:
                        manga_name = manga_name.replace(char, "")
                if manga_name not in manga_chapters_dict.keys():
                    LOG.debug(f"{manga_name} not in mangas.csv")
                    break
                else:
                    LOG.debug(f"Manga : {manga_name}")
                    link = manga.find('a')['href']
                    # extract the chapter and his link
                    chapter_link = "https://mangamoins.shaeishu.co/download" + link
                    chapter_element = manga.find('div', class_="sortiefooter")
                    chapter = "chapitre " + chapter_element.find('h3').text.replace("#", "")
                    manga_chapters_dict[manga_name].add(chapter)
                    chapters_and_links.append(["mangamoins", manga_name, chapter, chapter_link])
                    LOG.debug(f"{chapter} added | link : {chapter_link}")
            page += 1

        except Exception as e:
            LOG.debug(f"Error : {e} | {url}")
            return "failed"

    for index, manga_name in enumerate(manga_chapters_dict.keys()):
        manga_chapters_dict[manga_name] = list(manga_chapters_dict[manga_name])
        manga_chapters_dict[manga_name].sort(key=lambda x: float(x.split()[1]), reverse=True)
        datas.loc[index, 'n_chapter'] = len(manga_chapters_dict[manga_name])
        LOG.debug(f"{manga_name} : {len(manga_chapters_dict[manga_name])} chapters fetched.")

    links_dataframe = pd.DataFrame(chapters_and_links, columns=columns)
    links_dataframe.to_csv(f'{PATH_TO_MANGAMOINS}/datas/chapters_links.csv', index=False)

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_MANGAMOINS}/datas/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)

    datas.to_csv(f'{PATH_TO_MANGAMOINS}/datas/mangas.csv', index=False)
    return "success"
