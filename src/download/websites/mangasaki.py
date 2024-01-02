import requests
from selenium.webdriver.common.by import By
from src.foundation.core.essentials import SELECTOR, LOG
from src.foundation.core.emojis import EMOJIS


def init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name, DRIVER):
    """Initialize the download from mangasaki.

    Args:
        selected_website (str): selected website
        chapter_file_path (str/Path): path of the folder where to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name
        DRIVER (Any): the chromedriver

    Returns:
        str: download status (success, skipped or failed)
    """

    page = 0
    query = "SELECT ChapterLink FROM ChapterLink WHERE NomManga = ? AND NomSite = ? AND Chapitres = ?"
    SELECTOR.execute(query, (selected_manga_name, selected_website, chapter_name))
    chapter_link = SELECTOR.fetchone()[0]
    try:
        DRIVER.get(chapter_link)
        main_element = DRIVER.find_element(By.ID, 'images')
        img_elements = main_element.find_elements(By.TAG_NAME, 'img')

        if not isinstance(chapter_file_path, str):
            chapter_file_path = chapter_file_path._str

        if img_elements == []:
            LOG.debug(f"Download aborted {EMOJIS[4]}, no images found. | {chapter_link}")
            return "failed"

        for img in img_elements:
            img_url = img.get_attribute('src')
            save_path = f"{chapter_file_path}/{page}.jpg"
            response = mangasaki(img_url, save_path, page)
            if response is False:
                LOG.debug(f"Download aborted {EMOJIS[4]}")
                return "failed"
            page += 1
        LOG.debug(f"{chapter_name} downloaded {EMOJIS[3]}")
        return "success"

    except Exception as e:
        LOG.debug(f"{e} | {selected_manga_name} | {chapter_name}")
        return "failed"


def mangasaki(img_url, save_path, page):
    """Download images from mangasaki with the given URL.

    Args:
        img_url (str): image url
        save_path (str): path to save images
        page (int): page number to download

    Returns:
        bool: True(download successful), False(otherwise)
    """

    try:
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(img_response.content)
        else:
            LOG.debug(f"Image {page} failed to be downloaded | Status Code : {img_response.status_code}")
            return False
    except Exception as e:
        LOG.debug(f"Image {page} failed to be downloaded | {e}")
        return False
    LOG.debug(f"Image {page} downloaded")
    return True
