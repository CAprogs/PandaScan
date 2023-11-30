import requests
from lxml import html
from foundation.core.essentials import LOG


def init_download(selected_website, chapter_name_path, selected_manga_name, download_id, chapter_number):
    """initialiser le téléchargement à partir de fmteam.

    Args:
        selected_website (str): site web sélectionné
        chapter_name_path (str): chemin de sauvegarde des images
        selected_manga_name (str): nom du manga sélectionné
        download_id (int): numéro du téléchargement en cours
        chapter_number (str): numéro du chapitre à télecharger
    """

    page = 0
    chapter_link = str(f"https://scantrad-vf.co/manga/{selected_manga_name}/{chapter_number}/?style=list")
    try:
        http_response = requests.get(chapter_link)
        if http_response.status_code == 200:
            while True:
                xpath = f'//*[@id="image-{page}"]'
                save_path = f"{chapter_name_path}/{page}.jpg"
                response = scantrad(http_response, xpath, save_path, page)
                if response is True:
                    page += 1
                else:
                    LOG.debug(f"{chapter_number} downloaded ✅")
                    return "success"
        else:
            LOG.debug(f"Download {download_id} aborted ❌, Status code : {http_response.status_code}")
            return "failed"
    except requests.ConnectionError as e:
        LOG.debug(f"Request failed : {selected_website} | {selected_manga_name} | {chapter_number}\n Error : {e}")
        return "failed"


def scantrad(http_response, xpath, save_path, page):
    """Download images from scantrad with the given URL.

    Args:
        http_response (int): réponse de la requête HTTP
        xpath (str): xpath des images
        save_path (str): chemin de sauvegarde des images
        page (int): numéro de la page à télécharger

    Returns:
        bool: True(téléchargement réussi), False(téléchargement raté)
    """

    tree = html.fromstring(http_response.content)
    image_element = tree.xpath(xpath)
    if image_element:
        image_url = image_element[0].get('src')
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(image_response.content)
            LOG.debug(f"Image {page} téléchargée.")
            return True
        else:
            LOG.debug(f"Failed downloading Image {page}. Statut Code : {image_response.status_code}")
            return False
    else:
        LOG.debug("No element found for the xpath | scantrad")
        return False
