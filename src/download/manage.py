from src.download.websites import scantrad
from src.download.websites import lelscans
from src.download.websites import fmteam
from src.download.websites import animesama
from src.download.websites import tcbscans
from src.download.websites import lelmanga
from src.download.utils import check_manga_path


def download(selected_website, chapter_file_path, selected_manga_name, chapter_name, DRIVER):
    """Manage the right download for a specific website.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder where to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name
        DRIVER (ANY): the chromedriver

    Returns:
        str: download status (success, skipped, or failed)
    """

    if check_manga_path(chapter_file_path):
        return "skipped"

    if selected_website == "scantrad":
        status = scantrad.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "lelscans":
        status = lelscans.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "fmteam":
        status = fmteam.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name, DRIVER)

    elif selected_website == "animesama":
        status = animesama.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "tcbscans":
        status = tcbscans.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "lelmanga":
        status = lelmanga.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    return status
