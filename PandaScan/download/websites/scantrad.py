import requests
import os
from lxml import html
from foundation.core.essentials import LOG


def init_download(selected_website, chapter_name_path, selected_manga_name, download_id, chapter_name, chapter_number):
    """initialiser le téléchargement à partir de fmteam.

    Args:
        selected_website (str): site web sélectionné
        chapter_name_path (str): chemin de sauvegarde des images
        selected_manga_name (str): nom du manga sélectionné
        download_id (int): numéro du téléchargement en cours
        chapter_name (str): nom du chapitre
        chapter_number (str): numéro du chapitre à télecharger

    Returns:
        str: (Error message) if the method has failed.
    """

    if not os.path.exists(chapter_name_path):
        os.makedirs(chapter_name_path)
        page = 0
        chapter_link = str(f"https://scantrad-vf.co/manga/{selected_manga_name}/{chapter_number}/?style=list")
        try:
            http_response = requests.get(chapter_link)
            while True:
                xpath = f'//*[@id="image-{page}"]'
                save_path = f"{chapter_name_path}/{page}.jpg"
                response = scantrad(http_response, xpath, save_path, page)
                if response is True:
                    page += 1
                else:
                    LOG.debug(f"Téléchargement {download_id} terminé.")
                    break
        except requests.ConnectionError as e:
            LOG.debug(f"Requests failed : {selected_website} | {selected_manga_name} | {chapter_number}\n Error : {e}")
    else:
        LOG.debug(f"Le {chapter_name} du manga : {selected_manga_name} est déjà téléchargé !")


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

    if http_response.status_code == 200:
        # Parser le contenu HTML
        tree = html.fromstring(http_response.content)
        # Trouver l'élément à partir du xpath donné
        image_element = tree.xpath(xpath)
        if image_element:
            # Extraire l'URL de l'image à partir de l'attribut 'src'
            image_url = image_element[0].get('src')
            # Télécharger l'image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Sauvegarder l'image dans le fichier spécifié
                with open(save_path, 'wb') as f:
                    f.write(image_response.content)
                LOG.debug(f"Image {page} téléchargée.")
                return True
            else:
                LOG.debug(f"Échec du téléchargement de l'image. Code d'état : {image_response.status_code}")
                return False
        else:
            LOG.debug("Aucun élément trouvé pour le xpath donné.")
            return False
    else:
        LOG.debug(f"Échec de la requête HTTP.| Code d'état : {http_response.status_code}")
        return False
