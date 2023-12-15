from src.download.websites import scantrad
from src.download.websites import lelscans
from src.download.websites import fmteam
from src.download.websites import animesama
from src.download.websites import tcbscans
from src.download.utils import chapter_transform, check_manga_path


def download(selected_website, chapter_file_path, selected_manga_name, chapter_name, manga_file_path):
    """Manage the right download for a specific website.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name
        manga_file_path (str): path of the folder to save chapters

    Returns:
        str: download status (success, skipped, or failed)
    """

    if selected_website != "fmteam":
        if check_manga_path(chapter_file_path):
            return "skipped"

    chapter_number = chapter_transform(chapter_name, selected_website)

    if selected_website == "scantrad":
        status = scantrad.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_number)

    elif selected_website == "lelscans":
        status = lelscans.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_number)

    elif selected_website == "fmteam":
        status = fmteam.init_download(selected_website, manga_file_path, selected_manga_name, chapter_number)

    elif selected_website == "animesama":
        status = animesama.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)
    
    elif selected_website == "tcbscans":
        status = tcbscans.init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name)

    return status
