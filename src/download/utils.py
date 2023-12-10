import requests
import os
from src.foundation.core.essentials import LOG
from src.foundation.core.emojis import EMOJIS


def chapter_transform(chapter_name, selected_website):
    """Transform the chapter name to the right format.

    Args:
        chapter_name (str): chapter name
        selected_website (str): selected website

    Returns:
        str: chapter name in the right format
    """

    if selected_website == "scantrad":
        result = chapter_name.replace(' ', '-')
        return result
    else:
        result = chapter_name.replace('chapitre ', '')
        return result


def check_tome(selected_manga_name, selected_website, CURSOR):
    """Check if the manga contains "tomes".

    Args:
        selected_manga_name (str): selected manga name
        conn (Any): DB connection
        CURSOR (Any): DB cursor

    Returns:
        bool: True(the manga includes "tomes"), False(otherwise)
        str: the last "tome" of the manga
    """
    CURSOR.execute("SELECT has_tome FROM Mangas WHERE NomManga = ? AND NomSite = ?", (selected_manga_name, selected_website))
    try:
        has_tome = CURSOR.fetchone()[0]
        if has_tome.lower() == "yes":
            CURSOR.execute("SELECT last_tome FROM Mangas WHERE NomManga = ? AND NomSite = ?", (selected_manga_name, selected_website))
            last_tome = CURSOR.fetchone()[0]
            return True, last_tome
        else:
            return False, None
    except CURSOR.Error as e:
        LOG.debug(f"Fmteam - {selected_manga_name} can't be accessed.\n Error : {e}")

    return False, None


def check_url(pattern, tome, selected_manga_name, chapter_number):
    """Search a valid url for a specific manga.

    Args:
        pattern (str): used prefix for donwloads
        tome (str): the last "tome" of the manga
        selected_manga_name (str): selected manga name
        chapter_number (int): chapter number

    Returns:
        str: the valid url
        None: if no valid url is found
    """
    for i in range(int(float(tome)), -1, -1):
        if "." in chapter_number:
            chapter_number_1, chapter_number_2 = chapter_number.split(".")
            url = str(f"{pattern}{selected_manga_name}/fr/vol/{i}/ch/{chapter_number_1}/sub/{chapter_number_2}")
        else:
            url = str(f"{pattern}{selected_manga_name}/fr/vol/{i}/ch/{chapter_number}")
        response = requests.head(url)
        if response.status_code == 200:
            LOG.debug(f"""Valid address found {EMOJIS[3]}:
                url : {url}
                manga : {selected_manga_name}
                tome : {i}
                chapitre : {chapter_number}
                """)
            return url
    else:
        return None


def check_manga_path(chapter_file_path, download_id):
    """Check if the manga path exists.

    Args:
        chapter_file_path (str): path of the folder to save images
        download_id (int): current download number

    Returns:
        bool: True(manga already exists), False(otherwise)
    """
    if not os.path.exists(chapter_file_path):
        os.makedirs(chapter_file_path)
        return False
    else:
        LOG.debug(f"Download {download_id} skipped !\n\nChapter found in : {chapter_file_path}")
        return True
