import requests
from bs4 import BeautifulSoup
from foundation.core.essentials import SELECTOR
from foundation.core.essentials import LOG
from foundation.core.emojis import EMOJIS


def init_download(selected_website, chapter_file_path, selected_manga_name, download_id, chapter_name):
    """Initialize the download from animesama.

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
    query = "SELECT ChapterLink FROM ChapterLink WHERE NomManga = ? AND NomSite = ? AND Chapitres = ?"
    SELECTOR.execute(query, (selected_manga_name, selected_website, chapter_name))
    chapter_link = SELECTOR.fetchone()[0]
    try:
        http_response = requests.get(chapter_link)
        if http_response.status_code == 200:
            soup_1 = BeautifulSoup(http_response.text, "html.parser")
            select_element = soup_1.select_one('#readerarea')
            expected_imgs = str(select_element.contents).count('<img')
            img_elements = select_element.find("p")

            soup_2 = BeautifulSoup(img_elements.text, "html.parser")
            img_list = soup_2.find_all('img', {'data-src': True})
            if img_list == []:
                img_elements = img_elements.contents
                img_nb = str(img_elements).count('<img')
                if img_elements == [] or '<img' not in str(img_elements) or img_nb != expected_imgs:
                    separator_list = select_element.find_all(class_='separator')
                    img_elements = [element.contents[0] for element in separator_list]
                img_list = [element for element in img_elements if '<img' in str(element)]
                if len(img_list) != expected_imgs:
                    LOG.debug(f"Download {download_id} aborted | {chapter_name} | some images are missing {EMOJIS[10]}")
                    return "failed"

            for img in img_list:
                try:
                    img_link = img['data-src']
                except KeyError:
                    try:
                        img_link = img.contents[0]['data-src']
                    except Exception as e:
                        LOG.debug(f"Download {download_id} aborted | {chapter_name} | Error : {e}")
                        return "failed"
                save_path = f"{chapter_file_path}/{page}.jpg"
                response = animesama(img_link, save_path, page)
                if response is False:
                    LOG.debug(f"Download {download_id} aborted {EMOJIS[4]}, request failed.")
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


def animesama(img_link, save_path, page):
    """Download images from animesama with the given URL.

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
