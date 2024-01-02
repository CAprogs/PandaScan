import requests
import zipfile
import io
from src.foundation.core.essentials import SELECTOR
from src.foundation.core.essentials import LOG
from src.foundation.core.emojis import EMOJIS


def init_download(selected_website, chapter_file_path, selected_manga_name, chapter_name):
    """Initialize the download from mangamoins.

    Args:
        selected_website (str): selected website
        chapter_file_path (str): path of the folder where to save images
        selected_manga_name (str): selected manga name
        chapter_name (str): chapter name

    Returns:
        str: download status (success or failed)
    """

    query = "SELECT ChapterLink FROM ChapterLink WHERE NomManga = ? AND NomSite = ? AND Chapitres = ?"
    SELECTOR.execute(query, (selected_manga_name, selected_website, chapter_name))
    chapter_link = SELECTOR.fetchone()[0]

    try:
        http_response = requests.get(chapter_link)
        if http_response.status_code == 200:
            response = mangamoins(http_response, chapter_file_path)
            if response is True:
                LOG.debug(f'{chapter_name} downloaded {EMOJIS[3]}')
                return "success"
            elif response is False:
                LOG.debug(f"Download aborted , request failed {EMOJIS[4]}")
                return "failed"
        else:
            LOG.debug(f"Request failed | Status code : {http_response.status_code}")
            return "failed"
    except requests.ConnectionError as e:
        LOG.debug(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_name}\n Error : {e}")
        return "failed"


def mangamoins(http_response, chapter_file_path):
    """Download images from mangamoins with the given URL.

    Args:
        http_response (int): HTTP response code
        chapter_file_path (str): path of the folder where to save images

    Returns:
        bool: True(download successful), False(otherwise)
    """

    # Créer un flux binaire avec io.BytesIO à partir du contenu de la réponse
    zip_stream = io.BytesIO(http_response.content)
    # Créer un objet zipfile.ZipFile à partir du flux binaire
    with zipfile.ZipFile(zip_stream, "r") as zip_ref:
        namelist = zip_ref.namelist()
        if namelist:
            zip_ref.extractall(chapter_file_path)
            return True
        else:
            return False
