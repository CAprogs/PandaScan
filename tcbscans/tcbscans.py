import requests
from bs4 import BeautifulSoup
#from src.foundation.core.essentials import SELECTOR
#from src.foundation.core.essentials import LOG
#from src.foundation.core.emojis import EMOJIS


def init_download(selected_website, chapter_file_path, selected_manga_name, download_id, chapter_name):
    """Initialize the download from tcbscans.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder to save images
        selected_manga_name (str): selected manga name
        download_id (int): current download number
        chapter_name (str): chapter name

    Returns:
        str: download status (success or failed)
    """

    page = 0
    #query = "SELECT ChapterLink FROM ChapterLink WHERE NomManga = ? AND NomSite = ? AND Chapitres = ?"
    #SELECTOR.execute(query, (selected_manga_name, selected_website, chapter_name))
    #chapter_link = SELECTOR.fetchone()[0]
    chapter_link = "https://tcbscans.com/chapters/4285/black-clover-chapter-338-review-1687770237"
    try:
        http_response = requests.get(chapter_link)
        if http_response.status_code == 200:
            soup_1 = BeautifulSoup(http_response.text, "html.parser")
            select_element = soup_1.select_one('body > main > div.overflow-hidden > div.flex.flex-col.items-center.justify-center')
            expected_imgs = str(select_element.contents).count('<img')
            picture_elements = select_element.find_all("picture", class_="fixed-ratio")

            if picture_elements != [] and len(picture_elements) == expected_imgs:
                img_list = [element for element in picture_elements for element in element.contents if '<img' in str(element)]
                if len(img_list) != expected_imgs:
                    print(f"Download {download_id} aborted | {chapter_name} | some images are missing ") #{EMOJIS[10]}
                    return "failed"
            else:
                print(f"Download {download_id} aborted | {chapter_name} | some images are missing ") #{EMOJIS[10]}
                return "failed"

            for img in img_list:
                try:
                    img_link = img['src']
                except Exception as e:
                    print(f"Download {download_id} aborted | {chapter_name} | Error : {e}")
                    return "failed"
                save_path = f"{chapter_file_path}/{page}.jpg"
                response = tcbscans(img_link, save_path, page)
                if response is False:
                    print(f"Download {download_id} aborted , request failed.") #{EMOJIS[4]}
                    return "failed"
                page += 1
            print(f"{chapter_name} downloaded ") #{EMOJIS[3]}
            return "success"
        else:
            print(f"Request failed | Status code : {http_response.status_code}")
            return "failed"
    except requests.ConnectionError as e:
        print(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_name}\n Error : {e}")
        return "failed"


def tcbscans(img_link, save_path, page):
    """Download images from tcbscans with the given URL.

    Args:
        img_link (str): image download link
        save_path (str): path to save images
        page (int): page number to download

    Returns:
        bool: True(download successful), False(otherwise)
    """

    image_response = requests.get(img_link)
    if image_response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(image_response.content)
        print(f"Image {page} downloaded")
        return True
    else:
        print(f"Failed downloading Image {page}. Status code : {image_response.status_code}")
        return False
