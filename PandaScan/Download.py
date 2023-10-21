import os
import requests
import zipfile
import io
from lxml import html
from bs4 import BeautifulSoup

# Fonction pour attribuer le bon format au chapitre / volume
def chapter_transform(chapter_name, selected_website):
    """Transform the chapter name to the right format.

    Args:
        chapter_name (str): le nom du chapitre
        selected_website (str): le site web sélectionné

    Returns:
        str: le bon format du chapitre
    """    

    if selected_website == "scantrad-vf":
        result = chapter_name.replace(' ','-')
        return result
    elif selected_website == "lelscans.net" or selected_website == "fmteam.fr":
        result = chapter_name.replace('chapitre ','')
        return result

def check_tome(manga_current_name, selected_website, cursor):
    """Check if the manga contains tomes.

    Args:
        manga_current_name (str): le manga qu'on veut vérifier
        conn (sqlite3.connect): connexion à la base de données
        cursor (conn.cursor): curseur de la connexion
    """    
    cursor.execute("SELECT has_tome FROM Mangas WHERE NomManga = ? AND NomSite = ?", (manga_current_name,selected_website))
    try:
        has_tome = cursor.fetchone()[0]
        if has_tome.lower() == "yes":
            cursor.execute("SELECT last_tome FROM Mangas WHERE NomManga = ? AND NomSite = ?", (manga_current_name,selected_website))
            last_tome = cursor.fetchone()[0]
            return True, last_tome
        else:
            return False, None
    except:
        print(f"\nError check_tome() || fmteam - {manga_current_name} can't be accessed.")
    
    return False, None

def check_url(pattern, tome, manga_current_name, chapter_number):
    """Search a valid url for the specific manga.

    Args:
        pattern (str): le prefixe utilisé pour les téléchargements
        tome (str): le dernier tome du manga
        manga_current_name (str): le manga qu'on veut vérifier
        chapter_number (int): le numéro du chapitre
    """    
    
    for i in range(int(tome), -1, -1):                                                  # Définir la plage de recherche du bon tome
        url = str(f"{pattern}{manga_current_name}/fr/vol/{i}/ch/{chapter_number}")
        response = requests.head(url)                                                   # On Utilise HEAD pour vérifier l'existence de la ressource sans la télécharger
        if response.status_code == 200:                                                 # Si la ressource existe
            print(f"""Adresse valide trouvée ✅:
                url : {url} 
                manga : {manga_current_name}
                tome : {i}
                chapitre : chapitre {chapter_number}
                  """)
            return url
    else:
        return None


# ################################################################### Download Methods ####################################################################
# =========================================================================================================================================================

# ========================================================== Download Method ( SCANTRAD-VF ) 
def scantrad_download(response_url, xpath, save_path, page):
    """Download the images from the given URL.

    Args:
        response_url (_type_): _description_
        xpath (_type_): _description_
        save_path (_type_): _description_
        page (_type_): _description_

    Returns:
        _type_: _description_
    """    

    if response_url.status_code == 200:
        # Parser le contenu HTML
        tree = html.fromstring(response_url.content)
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
                print(f"Image {page} téléchargée.")                                                                         ##### Track activity
                return True
            else:
                print(f"Échec du téléchargement de l'image. Code d'état : {image_response.status_code}")                    ##### Track activity
                return False
        else:
            print("Aucun élément trouvé pour le xpath donné.")                                                              ##### Track activity
            return False
    else:
        print(f"Échec de la requête HTTP.| Code d'état : {response_url.status_code}")                                       ##### Track activity
        return False

# ========================================================== Download Method ( LELSCANS.NET ) 
def lelscans_download(response_url, save_path, page):
    """Download the images from the given URL.

    Args:
        response_url (_type_): _description_
        save_path (_type_): _description_
        page (_type_): _description_

    Returns:
        _type_: _description_
    """    

    if response_url.status_code == 200:
        # Parser le contenu HTML
        soup = BeautifulSoup(response_url.content, "html.parser")
        
        image_element = soup.find("img", src=True)
        if image_element:
            image_url = image_element["src"]

            # Télécharger l'image
            image_response = requests.get('https://lelscans.net/'+image_url)

            if image_response.status_code == 200:
                # Sauvegarder l'image dans le fichier spécifié
                with open(save_path, 'wb') as f:
                    f.write(image_response.content)
                print(f"Image {page} téléchargée.")                                         ##### Track activity
                return True
            else:
                print(f"Échec du téléchargement de l'image. Code d'état : {image_response.status_code}")                    ##### Track activity
                return False
        else:
            print("Aucun élément trouvé.")                                                 ##### Track activity
            return False
    else:
        print(f"Échec du téléchargement.| Code d'état : {response_url.status_code}")
        return False

# ========================================================== Download Method ( FMTEAM.FR ) 
def fmteam_download(response_url, nom_fichier, config):
    """Download the images from the given URL.

    Args:
        response_url (_type_): _description_
        nom_fichier (_type_): _description_
        config (_type_): _description_

    Returns:
        _type_: _description_
    """    

    if response_url.status_code == 200:
        # Utiliser io.BytesIO pour créer un flux binaire à partir du contenu de la réponse
        zip_stream = io.BytesIO(response_url.content)
        # Créer un objet zipfile.ZipFile à partir du flux binaire
        with zipfile.ZipFile(zip_stream, "r") as zip_ref:
            namelist = zip_ref.namelist()
            if namelist:
                # Obtenir le nom du premier fichier/dossier dans la liste
                first_file = namelist[0]
                file_name, useless = first_file.split("/")
                if os.path.exists(config['Download']['path']): 
                    file_name_path = nom_fichier + '/' + file_name
                else:
                    file_name_path = nom_fichier / file_name 
                
                if not os.path.exists(file_name_path):
                    zip_ref.extractall(nom_fichier)
                    return True
                else:
                    return False
    else:
        print("Échec du téléchargement.")


# ############################################################# Initialize Download Methods ###############################################################
# =========================================================================================================================================================

def Initialize_Download(selected_website, nom_chapitre, manga_current_name, chapter_number, current_download, chapter_name, nom_fichier, config, cursor):
    """Initialize the download of the images from the given URL.

    Args:
        selected_website (str): _description_
        nom_chapitre (str): _description_
        manga_current_name (srt): _description_
        chapter_number (str): _description_
        current_download (int): _description_
        chapter_name (str): _description_
        nom_fichier (str): _description_
        config (json): _description_
    """    

    # =============================================================  SCANTRAD-VF
    if selected_website == "scantrad-vf":
        if not os.path.exists(nom_chapitre):
            os.makedirs(nom_chapitre)
            page = 0 # Page de départ
            lien_chapitre = str(f"https://scantrad-vf.co/manga/{manga_current_name}/{chapter_number}/?style=list")  # Lien du chapitre
            try:
                response_url = requests.get(lien_chapitre) # Effectuer une requête HTTP sur l'URL donnée
                while True: # Téléchargement des images
                    xpath = f'//*[@id="image-{page}"]'
                    save_path = f"{nom_chapitre}/{page}.jpg"  # Chemin où sauvegarder les images
                    response = scantrad_download(response_url, xpath, save_path, page)
                    if response == True:
                        page += 1
                    else:
                        print(f"\nTéléchargement {current_download} terminé.\n")                                    ##### Track activity
                        break
            except:
                print(f"REQUEST ERROR INFOS : {selected_website} | {manga_current_name} | {chapter_number}")              ##### Track activity
        else:
            print(f"Le {chapter_name} du manga : {manga_current_name} est déjà téléchargé !")  # ON NE TÉLÉCHARGE PLUS INUTILEMENT LES MANGAS DÉJÀ TÉLÉCHARGÉS

    # =============================================================  LELSCANS.NET
    elif selected_website == "lelscans.net":
        if not os.path.exists(nom_chapitre):
            os.makedirs(nom_chapitre)
            page = 1 # Page de départ

            while True:                                                                                                       # Téléchargement des images
                lien_chapitre = str(f"https://lelscans.net/scan-{manga_current_name}/{chapter_number}/{page}")                # Lien du chapitre
                try:
                    response_url = requests.get(lien_chapitre)                                                                # Effectuer une requête HTTP sur l'URL donnée
                    save_path = f"{nom_chapitre}/{page}.jpg"                                                                  # Chemin où sauvegarder les images
                    response = lelscans_download(response_url, save_path, page)
                    if response == True:
                        page += 1
                    else:
                        print(f"\nTéléchargement {current_download} terminé.\n")                                              ##### Track activity
                        break
                except:
                    print(f"REQUEST ERROR INFOS : {selected_website} | {manga_current_name} | {chapter_number}")              ##### Track activity
        else:
            print(f"Le {chapter_name} du manga : {manga_current_name} est déjà téléchargé !")
    
    # =============================================================  FMTEAM.FR
    elif selected_website == "fmteam.fr":
        pattern = "https://fmteam.fr/api/download/"                                         # Pattern pour les téléchargements depuis fmteam.fr
        check, tome = check_tome(manga_current_name, selected_website, cursor)              # verifier si le manga sélectionné comprend des tomes
        if check == True and tome != None:                                                  # Si le manga comprend des tomes
            lien_chapitre = check_url(pattern, tome, manga_current_name, chapter_number)    # Chercher un lien valide pour le manga sélectionné
            if lien_chapitre == None:                                                       # Si aucun lien valide n'est trouvé
                return "No valid url found. ⚠️ | fmteam.fr | " + manga_current_name + " | chapitre" + chapter_number
        elif "." in chapter_number:                                                         # Si le numéro du chapitre comprend un point
            chapter_number_1, chapter_number_2 = chapter_number.split(".")
            lien_chapitre = str(f"{pattern}{manga_current_name}/fr/ch/{chapter_number_1}/sub/{chapter_number_2}")
        else:
            lien_chapitre = str(f"{pattern}{manga_current_name}/fr/ch/{chapter_number}")
        try:
            response_url = requests.get(lien_chapitre)                                      # Effectuer une requête HTTP sur l'URL donnée
            response = fmteam_download(response_url, nom_fichier, config)
            if response == True:
                print(f"\nTéléchargement {current_download} terminé. ✅\n")                                                                   ##### Track activity         
            else:
                print(f"\nTéléchargement {current_download} impossible ❌ OU dossier déjà existant. 🤔\n")                                    ##### Track activity
        except:
            print(f"REQUEST ERROR INFOS : {selected_website} | {manga_current_name} | {chapter_number}")                                     ##### Track activity

    # =============================================================  OTHER
    else:
        None     ############ Add another method for another website here ###########


# Uncomment to Debug
'''
from App import config, conn, cursor

selected_website = 'fmteam.fr' # fmteam.fr or lelscans.net or scantrad-v
nom_chapitre = '/Users/charles-albert/Desktop/chapitre 372' # see manga datas corresponding to the website
manga_current_name = 'berserk' # see datas corresponding to the website
chapter_number = '372' 
current_download = '0'
chapter_name = 'chapitre 372'
nom_fichier = 'berserk'
Initialize_Download(selected_website, nom_chapitre, manga_current_name, chapter_number, current_download, chapter_name, nom_fichier, config, cursor)
'''