import os
from src.download.utils import set_download_path, find_latest_zip, extract_zip
from src.foundation.core.essentials import SELECTOR, LOG
from src.foundation.core.emojis import EMOJIS


def init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name, DRIVER):
    """Initialize the download from fmteam.

    Args:
        selected_website (str): selected website
        chapter_file_path (str/Path): path of the folder where to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name
        DRIVER (Any): the chromedriver

    Returns:
        str: download status (success, skipped or failed)
    """

    query = "SELECT ChapterLink FROM ChapterLink WHERE NomManga = ? AND NomSite = ? AND Chapitres = ?"
    SELECTOR.execute(query, (selected_manga_name, selected_website, chapter_name))
    chapter_link = SELECTOR.fetchone()[0]

    if not isinstance(chapter_file_path, str):
        chapter_file_path = chapter_file_path._str
    try:
        set_download_path(DRIVER, chapter_file_path)

        DRIVER.get(chapter_link)

        zip_file_path = find_latest_zip(chapter_file_path)

        if zip_file_path:
            # Extract the zip file content
            extract_zip(zip_file_path, chapter_file_path)
            os.remove(zip_file_path)
        else:
            LOG.debug(f"Download aborted {EMOJIS[4]}, no Zip file found.")
            return "failed"

        LOG.debug(f"{chapter_name} downloaded {EMOJIS[3]}")
        return "success"
    except Exception as e:
        LOG.debug(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_name}\n Error : {e}")
        return "failed"
