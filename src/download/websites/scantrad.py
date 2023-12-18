import requests
from lxml import html
from src.foundation.core.essentials import SELECTOR, LOG
from src.foundation.core.emojis import EMOJIS


def init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name):
    """Initialize the download from scantrad.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder where to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name

    Returns:
        str: download status (success or failed)
    """

    page = 0
    query = "SELECT ChapterLink FROM ChapterLink WHERE NomManga = ? AND NomSite = ? AND Chapitres = ?"
    SELECTOR.execute(query, (selected_manga_name, selected_website, chapter_name))
    chapter_link = SELECTOR.fetchone()[0] + "?style=list"
    try:
        http_response = requests.get(chapter_link)
        if http_response.status_code == 200:
            while True:
                xpath = f'//*[@id="image-{page}"]'
                save_path = f"{chapter_file_path}/{page}.jpg"
                response = scantrad(http_response, xpath, save_path, page)
                if response is True:
                    page += 1
                elif response is False and page >= 1:
                    LOG.debug(f"{chapter_name} downloaded {EMOJIS[3]}")
                    return "success"
                else:
                    LOG.debug(f"Request failed | {selected_website} | {selected_manga_name} | {chapter_name}")
                    return "failed"
        else:
            LOG.debug(f"Request failed : {selected_website} {EMOJIS[4]}, Status code : {http_response.status_code}")
            return "failed"
    except requests.ConnectionError as e:
        LOG.debug(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_name}\n Error : {e}")
        return "failed"


def scantrad(http_response, xpath, save_path, page):
    """Download images from scantrad with the given URL.

    Args:
        http_response (int): HTTP response code
        xpath (str): images xpath
        save_path (str): path of the folder to save images
        page (int): page number to download

    Returns:
        bool: True(download successful), False(otherwise)
    """

    tree = html.fromstring(http_response.content)
    image_element = tree.xpath(xpath)
    if image_element:
        image_url = image_element[0].get('src')
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(image_response.content)
            LOG.debug(f"Image {page} downloaded.")
            return True
        else:
            LOG.debug(f"Failed downloading Image {page}. Statut Code : {image_response.status_code}")
            return False
    else:
        LOG.debug("No element found for the xpath provided.")
        return False
