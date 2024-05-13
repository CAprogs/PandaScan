import requests
from bs4 import BeautifulSoup
from src.foundation.core.essentials import SELECTOR, LOG
from src.foundation.core.emojis import EMOJIS
from ..utils import fetch_chapterlink


def init_download(selected_website: str, chapter_file_path: str, selected_manga_name: str, chapter_name: str):
    """Initialize the download from lelscans.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder where to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name

    Returns:
        str: download status (success or failed)
    """

    page = 1
    url = fetch_chapterlink(SELECTOR, (selected_manga_name, selected_website, chapter_name))

    while True:
        chapter_link = url + f"/{page}"
        try:
            http_response = requests.get(chapter_link)
            if http_response.status_code == 200:
                save_path = f"{chapter_file_path}/{page}.jpg"
                response = lelscans(http_response, save_path, page)
                if response is True:
                    page += 1
                elif response is False and page >= 1:
                    LOG.debug(f"{chapter_name} downloaded {EMOJIS[3]}")
                    return "success"
                else:
                    LOG.debug(f"Request failed | {selected_website} | {selected_manga_name} | {chapter_name}")
                    return "failed"
            else:
                LOG.debug(f"Request failed | Status code : {http_response.status_code}")
                return "failed"
        except requests.ConnectionError as e:
            LOG.debug(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_name}\n Error : {e}")
            return "failed"


def lelscans(http_response: int, save_path: str, page: int):
    """Download images from lelscans with the given URL.

    Args:
        http_response (int): HTTP response code
        save_path (str): path of the folder to save images
        page (int): page number to download

    Returns:
        bool: True(download successful), False(otherwise)
    """

    soup = BeautifulSoup(http_response.content, "html.parser")

    image_element = soup.find("img", src=True)
    if image_element:
        image_url = image_element["src"]
        image_response = requests.get('https://lelscans.net/' + image_url)
        if image_response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(image_response.content)
            LOG.debug(f"Image {page} downloaded")
            return True
        else:
            LOG.debug(f"Failed downloading Image {page}. Status code : {image_response.status_code}")
            return False
    else:
        LOG.debug("No element found | lelscans")
        return False
