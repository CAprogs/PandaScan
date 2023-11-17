from download.websites import scantrad
from download.websites import lelscans
from download.websites import fmteam
from download.utils import chapter_transform


def download(selected_website, chapter_name_path, selected_manga_name, download_id, chapter_name, manga_file_path, SETTINGS, SELECTOR):
    """Manage the right download for a specific website.

    Args:
        selected_website (str): site web sélectionné
        chapter_name_path (str): chemin de sauvegarde des images
        selected_manga_name (str): nom du manga sélectionné
        download_id (int): numéro du téléchargement en cours
        chapter_name (str): nom du chapitre
        manga_file_path (str): nom du dossier du manga
        SETTINGS (Any): fichier de configuration json
        SELECTOR (Any): curseur de la DB
    """

    chapter_number = chapter_transform(chapter_name, selected_website)

    if selected_website == "scantrad":
        scantrad.init_download(selected_website, chapter_name_path, selected_manga_name, download_id, chapter_number)

    elif selected_website == "lelscans":
        lelscans.init_download(selected_website, chapter_name_path, selected_manga_name, download_id, chapter_number)

    elif selected_website == "fmteam":
        fmteam.init_download(selected_website, selected_manga_name, download_id, manga_file_path, SETTINGS, SELECTOR, chapter_number)
