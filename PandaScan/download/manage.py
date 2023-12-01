from download.websites import scantrad
from download.websites import lelscans
from download.websites import fmteam
from download.websites import animesama
from download.utils import chapter_transform, check_manga_path


def download(selected_website, chapter_file_path, selected_manga_name, download_id, chapter_name, manga_file_path, SETTINGS, SELECTOR):
    """Manage the right download for a specific website.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder to save images
        selected_manga_name (str): selected manga name
        download_id (int): current download number
        chapter_name (str): chapter name
        manga_file_path (str): path of the folder to save chapters
        SETTINGS (Any): json configuration file
        SELECTOR (Any): DB cursor

    Returns:
        str: download status (success, skipped, or failed)
    """

    if check_manga_path(chapter_file_path, download_id):  # don't affect fmteam
        return "skipped"

    chapter_number = chapter_transform(chapter_name, selected_website)

    if selected_website == "scantrad":
        status = scantrad.init_download(selected_website, chapter_file_path, selected_manga_name, download_id, chapter_number)

    elif selected_website == "lelscans":
        status = lelscans.init_download(selected_website, chapter_file_path, selected_manga_name, download_id, chapter_number)

    elif selected_website == "fmteam":
        status = fmteam.init_download(selected_website, selected_manga_name, download_id, manga_file_path, SETTINGS, SELECTOR, chapter_number)

    elif selected_website == "animesama":
        status = animesama.init_download(selected_website, chapter_file_path, selected_manga_name, download_id, chapter_name)

    return status
