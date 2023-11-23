import requests
import os
from bs4 import BeautifulSoup
from foundation.core.essentials import SELECTOR
from foundation.core.essentials import LOG


def init_download(selected_website, chapter_name_path, selected_manga_name, download_id, chapter_name):
    """Initialiser le téléchargement à partir de animesama.

    Args:
        selected_website (str): site web sélectionné
        chapter_name_path (str): chemin de sauvegarde des images
        selected_manga_name (str): nom du manga sélectionné
        download_id (int): numéro du téléchargement en cours
        chapter_name (str): nom du chapitre
    """

    if not os.path.exists(chapter_name_path):
        os.makedirs(chapter_name_path)
        page = 0
        query = "SELECT ChapterLink FROM ChapterLink WHERE NomManga LIKE ? AND NomSite = ? AND Chapitres = ?"
        SELECTOR.execute(query, (selected_manga_name, selected_website, chapter_name))
        chapter_link = SELECTOR.fetchone()[0]
        try:
            http_response = requests.get(chapter_link)
            if http_response.status_code == 200:
                soup_1 = BeautifulSoup(http_response.text, "html.parser")
                select_element = soup_1.select_one('#readerarea')
                img_elements = select_element.find("p")

                soup_2 = BeautifulSoup(img_elements.text, "html.parser")
                img_list = soup_2.find_all('img', {'data-src': True})

                for img in img_list:
                    img_link = img['data-src']
                    save_path = f"{chapter_name_path}/{page}.jpg"
                    response = animesama(img_link, save_path, page)
                    if response is False:
                        return LOG.info(f"Download {download_id} aborted ❌, request failed.")
                    page += 1
                LOG.debug(f"Download {download_id} completed ✅")
            else:
                LOG.debug(f"Échec de la requête HTTP.| Code d'état : {http_response.status_code}")
        except requests.ConnectionError as e:
            LOG.debug(f"Requests failed : {selected_website} | {selected_manga_name} | {chapter_name}\n Error : {e}")
    else:
        LOG.info(f"Download {download_id} skipped !\n\nChapter found at : {chapter_name_path}")


def animesama(img_link, save_path, page):
    """Download images from animesama with the given URL.

    Args:
        img_link (str): lien de téléchargement de l'image
        save_path (str): chemin de sauvegarde des images
        page (int): numéro de la page à télécharger

    Returns:
        bool: True(téléchargement réussi), False(téléchargement raté)
    """

    image_response = requests.get(img_link)
    if image_response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(image_response.content)
        LOG.debug(f"Image {page} téléchargée.")
        return True
    else:
        LOG.debug(f"Échec du téléchargement de l'image {page}. Code d'état : {image_response.status_code}")
        return False