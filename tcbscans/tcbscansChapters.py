import requests
import pandas as pd
import yaml
from bs4 import BeautifulSoup

PATH_TO_TCBSCANS = "/Users/charles-albert/Desktop/PandaScan/tests/tcbscans"

def Scrap_chapters():
    """Scrap the mangas chapters from tcbscans.

    Args:
        PATH_TO_TCBSCANS (str): path to tcbscans directory (update)
        LOG (Any): the logger
    """

    datas = pd.read_csv(f'{PATH_TO_TCBSCANS}/mangas.csv')
    manga_chapters_dict = {}
    chapters_and_links = []
    last_manga_index = len(datas['NomManga'])-1
    columns = ["NomSite", "NomManga", "Chapitres", "ChapterLink"]
    failed_mangas = []

    for index, manga_name in enumerate(datas['NomManga']):
        url = datas['links'][index]

        try:
            response = requests.get(url)
            html_content = response.text
            soup_1 = BeautifulSoup(html_content, "html.parser")
            select_element = soup_1.select_one('body > main > div.overflow-hidden > div > div > div.col-span-2')
            if not select_element and last_manga_index != len(datas['NomManga'])-1:
                print(f"Error : No chapter found | {url} | tcbscans")
                continue

            print(f"Manga : {manga_name}")
            manga_chapters_dict[manga_name] = []
            chapters_elements = select_element.find_all("a")

            for element in chapters_elements:
                chapter_title = [element.text for element in element.contents if "text-lg font-bold" in str(element)]
                # extract the chapter and his link
                if chapter_title != []:
                    chapter = "chapter " + chapter_title[0].split("Chapter", 1)[1].strip()
                    chapter_link = 'https://tcbscans.com' + element['href']
                    manga_chapters_dict[manga_name].append(chapter)
                    chapters_and_links.append(["tcbscans", manga_name, chapter, chapter_link])
                    print(f"{chapter} added | link : {chapter_link}")
                else:
                    print(f"Error : {chapter_title} | {url} | tcbscans")

            print(f"{len(manga_chapters_dict[manga_name])} chapters fetched.")

        except Exception as e:
            if index != last_manga_index:
                print(f"Error : {e} | {url} | tcbscans | not the last manga")
                failed_mangas.append(manga_name)
                continue
            else:
                print(f"Error : {e} | {url} | tcbscans | {manga_name}")
                return

    links_dataframe = pd.DataFrame(chapters_and_links, columns=columns)
    links_dataframe.to_csv(f'{PATH_TO_TCBSCANS}/chapters_links.csv', index=False)

    yml_data = yaml.dump(manga_chapters_dict)
    with open(f'{PATH_TO_TCBSCANS}/mangas_chapters_temp.yml', 'w') as file:
        file.write(yml_data)
    
    print(f"\n{len(failed_mangas)} mangas failed :\n")
    for manga in failed_mangas:
        print(manga)


Scrap_chapters()
