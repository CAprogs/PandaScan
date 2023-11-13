import requests
import os
from bs4 import BeautifulSoup
from foundation.core.essentials import LOG


def init_download(selected_website, chapter_name_path, selected_manga_name, download_id, chapter_name, chapter_number):
    """initialiser le téléchargement à partir de lelscans.

    Args:
        selected_website (str): site web sélectionné
        chapter_name_path (str): chemin de sauvegarde des images
        selected_manga_name (str): nom du manga sélectionné
        download_id (int): numéro du téléchargement en cours
        chapter_name (str): nom du chapitre
        chapter_number (str): numéro du chapitre à télecharger
    """

    if not os.path.exists(chapter_name_path):
        os.makedirs(chapter_name_path)
        page = 1

        while True:
            chapter_link = str(f"https://lelscans.net/scan-{selected_manga_name}/{chapter_number}/{page}")
            try:
                http_response = requests.get(chapter_link)
                save_path = f"{chapter_name_path}/{page}.jpg"
                response = lelscans(http_response, save_path, page)
                if response is True:
                    page += 1
                else:
                    LOG.debug(f"Téléchargement {download_id} terminé.")
                    break
            except requests.ConnectionError as e:
                LOG.debug(f"Requests failed : {selected_website} | {selected_manga_name} | {chapter_number}\n Error : {e}")
    else:
        LOG.debug(f"Le {chapter_name} de {selected_manga_name} est déjà téléchargé !")


def lelscans(http_response, save_path, page):
    """Download images from lelscans with the given URL.

    Args:
        http_response (int): réponse de la requête HTTP
        save_path (str): chemin de sauvegarde des images
        page (int): numéro de la page à télécharger

    Returns:
        bool: True(téléchargement réussi), False(téléchargement raté)
    """

    if http_response.status_code == 200:
        # Parser le contenu HTML
        soup = BeautifulSoup(http_response.content, "html.parser")

        image_element = soup.find("img", src=True)
        if image_element:
            image_url = image_element["src"]

            # Télécharger l'image
            image_response = requests.get('https://lelscans.net/'+image_url)

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
            LOG.debug("Aucun élément trouvé.")
            return False
    else:
        LOG.debug(f"Échec du téléchargement.| Code d'état : {http_response.status_code}")
        return False
