import requests
from bs4 import BeautifulSoup
from src.foundation.core.essentials import SELECTOR
from src.foundation.core.essentials import LOG
from src.foundation.core.emojis import EMOJIS


def init_download(selected_website: str, chapter_file_path: str, selected_manga_name: str, chapter_name: str):
    """Initialize the download from lelmanga.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name

    Returns:
        str: download status (success or failed)
    """

    page = 0
    query = "SELECT ChapterLink FROM ChapterLink WHERE NomManga = ? AND NomSite = ? AND Chapitres = ?"
    SELECTOR.execute(query, (selected_manga_name, selected_website, chapter_name))
    chapter_link = SELECTOR.fetchone()[0]
    try:
        http_response = requests.get(chapter_link)
        if http_response.status_code == 200:
            soup_1 = BeautifulSoup(http_response.text, "html.parser")
            select_element = soup_1.select_one('#readerarea')
            expected_imgs = str(select_element.contents).count('<img')
            p_elements = select_element.find_all("p")

            if p_elements != [] and len(p_elements) == expected_imgs:
                img_elements = [element.contents[0] for element in p_elements]
                img_list = [element for element in img_elements if '<img' in str(element)]
                if len(img_list) != expected_imgs:
                    LOG.debug(f"Download aborted | {chapter_name} | some images are missing {EMOJIS[10]}")
                    return "failed"
            else:
                LOG.debug(f"Download aborted | {chapter_name} | some images are missing {EMOJIS[10]}")
                return "failed"

            for img in img_list:
                try:
                    img_link = img['src']
                except Exception as e:
                    LOG.debug(f"Download aborted | {chapter_name} | Error : {e}")
                    return "failed"
                save_path = f"{chapter_file_path}/{page}.jpg"
                response = lelmanga(img_link, save_path, page)
                if response is False:
                    LOG.debug(f"Download aborted , request failed {EMOJIS[4]}")
                    return "failed"
                page += 1
            LOG.debug(f"{chapter_name} downloaded {EMOJIS[3]}")
            return "success"
        else:
            LOG.debug(f"Request failed | Status code : {http_response.status_code}")
            return "failed"
    except requests.ConnectionError as e:
        LOG.debug(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_name}\n Error : {e}")
        return "failed"


def lelmanga(img_link: str, save_path: str, page: int):
    """Download images from lelmanga with the given URL.

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
        LOG.debug(f"Image {page} downloaded")
        return True
    else:
        LOG.debug(f"Failed downloading Image {page}. Status code : {image_response.status_code}")
        return False
