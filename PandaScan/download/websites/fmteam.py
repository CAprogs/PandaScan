
import requests
import zipfile
import io
import os
from download.utils import check_tome, check_url
from foundation.core.essentials import LOG
from foundation.core.emojis import EMOJIS


def init_download(selected_website, selected_manga_name, download_id, manga_file_path, SETTINGS, SELECTOR, chapter_number):
    """Initialize the download from fmteam.

    Args:
        selected_website (str): selected website
        selected_manga_name (str): selected manga name
        download_id (int): current download number
        manga_file_path (str): path of the folder to save chapters
        SETTINGS (Any): json configuration file
        SELECTOR (Any): DB cursor
        chapter_number (str): chapter number to download

    Returns:
        str: download status (success, skipped or failed)
    """

    pattern = "https://fmteam.fr/api/download/"
    check, tome = check_tome(selected_manga_name, selected_website, SELECTOR)
    if check is True and tome is not None:
        chapter_link = check_url(pattern, tome, selected_manga_name, chapter_number)
        if chapter_link is None:
            return LOG.debug(f"No valid url found. ⚠️ | fmteam.fr | {selected_manga_name} | chapitre {chapter_number}")
    elif "." in chapter_number:
        chapter_number_1, chapter_number_2 = chapter_number.split(".")
        chapter_link = str(f"{pattern}{selected_manga_name}/fr/ch/{chapter_number_1}/sub/{chapter_number_2}")
    else:
        chapter_link = str(f"{pattern}{selected_manga_name}/fr/ch/{chapter_number}")
    try:
        http_response = requests.get(chapter_link)
        if http_response.status_code == 200:
            response = fmteam(http_response, manga_file_path, SETTINGS)
            if response is True:
                LOG.debug(f"chapitre {chapter_number} downloaded {EMOJIS[3]}")
                return "success"
            elif response is False:
                LOG.debug(f"Download {download_id} aborted {EMOJIS[4]}, request failed.")
                return "failed"
            else:
                LOG.debug(f"Download {download_id} skipped !\n\nChapter found in : {response}")
                return "skipped"
        else:
            LOG.debug(f"Request failed : {selected_website} | {selected_manga_name}")
            return "failed"
    except requests.ConnectionError as e:
        LOG.debug(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_number}\n Error : {e}")
        return "failed"


def fmteam(http_response, manga_file_path, SETTINGS):
    """Download images from fmteam with the given URL.

    Args:
        http_response (int): HTTP response code
        manga_file_path (str): path of the folder to save chapters
        SETTINGS (Any): json configuration file

    Returns:
        bool: True(download successful), False(otherwise)
    """

    # Créer un flux binaire avec io.BytesIO à partir du contenu de la réponse
    zip_stream = io.BytesIO(http_response.content)
    # Créer un objet zipfile.ZipFile à partir du flux binaire
    with zipfile.ZipFile(zip_stream, "r") as zip_ref:
        namelist = zip_ref.namelist()
        if namelist:
            # Obtenir le nom du premier fichier/dossier dans la liste
            first_file = namelist[0]
            file_name, _ = first_file.split("/")
            if os.path.exists(SETTINGS['Download']['path']):
                file_name_path = manga_file_path + '/' + file_name
            else:
                file_name_path = manga_file_path / file_name

            if not os.path.exists(file_name_path):
                zip_ref.extractall(manga_file_path)
                return True
            else:
                return file_name_path
        else:
            return False
