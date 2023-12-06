import requests
from bs4 import BeautifulSoup
from foundation.core.essentials import LOG
from foundation.core.emojis import EMOJIS


def init_download(selected_website, chapter_file_path, selected_manga_name, download_id, chapter_number):
    """Initialize the download from lelscans.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder to save images
        selected_manga_name (str): selected manga name
        download_id (int): current download number
        chapter_number (str): chapter number to download

    Returns:
        str: download status (success or failed)
    """

    page = 1

    while True:
        chapter_link = str(f"https://lelscans.net/scan-{selected_manga_name}/{chapter_number}/{page}")
        try:
            http_response = requests.get(chapter_link)
            if http_response.status_code == 200:
                save_path = f"{chapter_file_path}/{page}.jpg"
                response = lelscans(http_response, save_path, page)
                if response is True:
                    page += 1
                else:
                    LOG.debug(f"chapitre {chapter_number} downloaded {EMOJIS[3]}")
                    return "success"
            else:
                LOG.debug(f"Request failed | Status code : {http_response.status_code}")
                return "failed"
        except requests.ConnectionError as e:
            LOG.debug(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_number}\n Error : {e}")
            return "failed"


def lelscans(http_response, save_path, page):
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
