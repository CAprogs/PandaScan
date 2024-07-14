from src.download.websites import lelscans, fmteam, tcbscans, lelmanga
from src.download.websites import manganelo, mangamoins, mangasaki, lhtranslation
from src.download.utils import check_manga_path


def download(selected_website: str, chapter_file_path: str, selected_manga_name: str, chapter_name: str, DRIVER):
    """Manage the right download for a specific website.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder where to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name
        DRIVER (Any): the chromedriver

    Returns:
        str: download status (success, skipped, or failed)
    """

    if check_manga_path(chapter_file_path):
        return "skipped"

    if selected_website == "lelscans":
        status = lelscans.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "fmteam":
        status = fmteam.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name, DRIVER)

    elif selected_website == "tcbscans":
        status = tcbscans.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "lelmanga":
        status = lelmanga.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "manganelo":
        status = manganelo.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "mangamoins":
        status = mangamoins.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    elif selected_website == "mangasaki":
        status = mangasaki.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name, DRIVER)

    elif selected_website == "lhtranslation":
        status = lhtranslation.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    else:
        status = "failed"

    return status
