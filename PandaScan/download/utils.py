import requests
from foundation.core.essentials import LOG


def chapter_transform(chapter_name, selected_website):
    """Transform the chapter name to the right format.

    Args:
        chapter_name (str): nom du chapitre
        selected_website (str): site web sélectionné

    Returns:
        str: numéro du chapitre
    """

    if selected_website == "scantrad":
        result = chapter_name.replace(' ', '-')
        return result
    else:
        result = chapter_name.replace('chapitre ', '')
        return result


def check_tome(selected_manga_name, selected_website, CURSOR):
    """Check if the manga contains tomes.

    Args:
        selected_manga_name (str): nom du manga sélectionné
        conn (Any): connexion à la DB
        CURSOR (Any): curseur de la DB

    Returns:
        bool: True(le manga comprend des tomes), False(le manga ne comprend pas de tomes)
        str: le dernier tome du manga
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
        pattern (str): prefixe utilisé pour les téléchargements
        tome (str): dernier tome du manga
        selected_manga_name (str): nom du manga sélectionné
        chapter_number (int): numéro du chapitre

    Returns:
        str: l'url valide
    """
    for i in range(int(float(tome)), -1, -1):
        if "." in chapter_number:
            chapter_number_1, chapter_number_2 = chapter_number.split(".")
            url = str(f"{pattern}{selected_manga_name}/fr/vol/{i}/ch/{chapter_number_1}/sub/{chapter_number_2}")
        else:
            url = str(f"{pattern}{selected_manga_name}/fr/vol/{i}/ch/{chapter_number}")
        response = requests.head(url)
        if response.status_code == 200:
            LOG.debug(f"""Valid address found ✅:
                url : {url}
                manga : {selected_manga_name}
                tome : {i}
                chapitre : {chapter_number}
                """)
            return url
    else:
        return None
