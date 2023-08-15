# ------------------------------------------------------------------------------------------------------------
# ____                     __               ____                               
#/\  _`\                  /\ \             /\  _`\                             
#\ \ \L\ \ __      ___    \_\ \     __     \ \,\L\_\    ___     __      ___    
# \ \ ,__/'__`\  /' _ `\  /'_` \  /'__`\    \/_\__ \   /'___\ /'__`\  /' _ `\  
#  \ \ \/\ \L\.\_/\ \/\ \/\ \L\ \/\ \L\.\_    /\ \L\ \/\ \__//\ \L\.\_/\ \/\ \ 
#   \ \_\ \__/.\_\ \_\ \_\ \___,_\ \__/.\_\   \ `\____\ \____\ \__/.\_\ \_\ \_\
#    \/_/\/__/\/_/\/_/\/_/\/__,_ /\/__/\/_/    \/_____/\/____/\/__/\/_/\/_/\/_/
#                                                                              
# ------------------------------------------------------------------------------------------------------------
# Welcome to PandaScan 🐼 | @2023 by CAprogs
# This is a project that aims to download mangas scans from a website by selecting the manga and chapters wished.
# scans are downloaded by a simple request.
# Ublock ( A Chrome Extension ) is recommand to use this Software.
# The Download Time depends on the number of Chapters to download and their Number of pages.
# Note 1 : Some websites may not provide accurate informations or may be empty. Another Features that permit to switch between websites for download will be available at the next update.
# Note 2 : An Update button will be available so your manga list can be up to date if there's new manga chapters availables ( Not available Yet )
# Credits: @Tkinter Designer by ParthJadhav 
# ------------------------------------------------------------------------------------------------------------

# Mettre à jour la docu 0/1
# Mettre à jour le bouton Update 0/2
# Migrer les dépendances de l'app dans des fichiers externes .py 0/-||-

# Importation des bibliothèques utiles
import os
import pandas as pd
import yaml
import tkinter as tk
import requests
import zipfile
import io
from lxml import html
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, StringVar, OptionMenu
from tkinter import messagebox
from tkinter.font import Font
from pathlib import Path
from bs4 import BeautifulSoup

################################ Variables Globales ############################################
All_chapters_len = 0    #  stocker le nombre de chapitres total d'un manga sélectionné
total_downloads = 0     #  stocker le nombre de téléchargements de Chapitres à effectuer
current_download = 0    #  variable d'incrémentation du nombre de téléchargements
manga_current_name = '' #  stocker le nom du manga sélectionné
chapters_current_selected = [] # stocker la liste des chapitres sélectionnés
Download_state = False # Etat du bouton Download
nom_fichier = '' # Chemin vers le fichier du manga à télécharger
selected_website = "scantrad-vf"
#################################################################################################

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# chemin relatif vers le dossier "frame0"
assets_directory = script_directory / "frame0"
mangas_path = script_directory / f"datas/{selected_website}/mangas.csv"
chapters_path = script_directory / f"datas/{selected_website}/mangas_chapters.yml"

# Chargement des datas ( par défaut )
with open(chapters_path, 'r') as file:
        chapitres = yaml.safe_load(file)
datas = pd.read_csv(mangas_path)

#################################################################################################

# Initialiser la fenêtre Tkinter
window = Tk()

# Donner un nom à la fenêtre
window.title("PandaScan 🐼")

# Paramètres par défaut de la fenêtre
window.geometry("962x686")
window.configure(bg = "#FFFFFF")
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 686,
    width = 962,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

# Définition de Fonts personnalisés
bold_font = Font(family="Arial", size=10) 

######################################################################   FONCTIONS  & CLASSES  ######################################################################
# Importation des éléments graphique
def relative_to_assets(path: str) -> Path:
    return assets_directory / Path(path)

# Action à effectuer à la fermeture de l'application
def on_closing():
    window.destroy() # Fermeture de la fenêtre tkinter

def Update_website(*args):
    global selected_website
    global mangas_path
    global chapters_path
    global chapitres
    global datas

    selected_item = website_list_var.get()
    selected_website = selected_item
    print(f"\nWebsite sélectionné : {selected_item}")                                               ##### Track activity
    
    mangas_path = script_directory / f"datas/{selected_website}/mangas.csv"
    chapters_path = script_directory / f"datas/{selected_website}/mangas_chapters.yml"

    with open(chapters_path, 'r') as file:
        chapitres = yaml.safe_load(file)
    datas = pd.read_csv(mangas_path)

    result_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste déroulante ( mangas list )
    chapters_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste déroulante ( chapters list )

# Mettre à jour les chapitres et mangas disponibles
def Update_datas():
    None

# Ajouter manuellement des mangas à la liste des mangas disponibles ( ajouter un bouton +)
def Add_mangas_to_list():  
    None

# Fonction pour attribuer le bon format au chapitre / volume
def chapter_transform(chapter_name):
    global selected_website

    if selected_website == "scantrad-vf":
        result = chapter_name.replace(' ','-')
        return result
    elif selected_website == "lelscans.net" or selected_website == "fmteam.fr":
        result = chapter_name.replace('chapitre ','')
        return result

# Download ou non les éléments sélectionnés
def show_Download_info():
    global current_download
    global total_downloads
    global All_chapters_len
    global nom_fichier

    # Réinitialiser les variables du téléchargement
    current_download = 0

    def Hide_DownloadBox():
        canvas.itemconfigure(image_1, state=tk.HIDDEN)

    # Fonction de téléchargement (scantrad-vf)
    def scantrad_download(response_url, xpath, save_path, page):

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
                    print(f"Image {page} téléchargée.")                                         ##### Track activity
                    return True
                else:
                    print(f"Échec du téléchargement de l'image. Code d'état : {image_response.status_code}")                    ##### Track activity
                    return False
            else:
                print("Aucun élément trouvé pour le xpath donné.")                              ##### Track activity
                return False
        else:
            print(f"Échec de la requête HTTP.| Code d'état : {response_url.status_code}")                        ##### Track activity
            return False
    
    # Fonction de téléchargement (lelscans.net)
    def lelscans_download(response_url, save_path, page):

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
    
    # Fonction de téléchargement (fmteam.fr)
    def fmteam_download(response_url, nom_fichier):

        if response_url.status_code == 200:
            # Utiliser io.BytesIO pour créer un flux binaire à partir du contenu de la réponse
            zip_stream = io.BytesIO(response_url.content)
            # Créer un objet zipfile.ZipFile à partir du flux binaire
            with zipfile.ZipFile(zip_stream, "r") as zip_ref:
                namelist = zip_ref.namelist()
                if namelist:
                    # Obtenir le nom du premier fichier/dossier dans la liste
                    first_file = namelist[0]
                    file_name, unecessary = first_file.split("/")
                    file_name_path = nom_fichier / file_name
                    if not os.path.exists(file_name_path):
                        zip_ref.extractall(nom_fichier)
                        return True
                    else:
                        return False
        else:
            print("Échec du téléchargement.")
    
    def Download():
        global chapters_current_selected
        global manga_current_name
        global current_download
        global nom_fichier
        global selected_website

        chapter_name = chapters_current_selected[current_download]  # Nom du Chapitre
        nom_chapitre = nom_fichier / chapter_name

        # Création du Dossier du chapitre correspondant s'il n'existe pas
        chapter_number = chapter_transform(chapter_name) # retourne le format adapté pour le site correspondant

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

        elif selected_website == "lelscans.net":
            if not os.path.exists(nom_chapitre):
                os.makedirs(nom_chapitre)
                page = 1 # Page de départ

                while True: # Téléchargement des images
                    lien_chapitre = str(f"https://lelscans.net/scan-{manga_current_name}/{chapter_number}/{page}")  # Lien du chapitre
                    try:
                        response_url = requests.get(lien_chapitre) # Effectuer une requête HTTP sur l'URL donnée
                        save_path = f"{nom_chapitre}/{page}.jpg"  # Chemin où sauvegarder les images
                        response = lelscans_download(response_url, save_path, page)
                        if response == True:
                            page += 1
                        else:
                            print(f"\nTéléchargement {current_download} terminé.\n")                                    ##### Track activity
                            break
                    except:
                        print(f"REQUEST ERROR INFOS : {selected_website} | {manga_current_name} | {chapter_number}")              ##### Track activity
            else:
                print(f"Le {chapter_name} du manga : {manga_current_name} est déjà téléchargé !")  # ON NE TÉLÉCHARGE PLUS INUTILEMENT LES MANGAS DÉJÀ TÉLÉCHARGÉS
        
        elif selected_website == "fmteam.fr":
    
            if "." in chapter_number:
                chapter_number_1, chapter_number_2 = chapter_number.split(".")
                lien_chapitre = str(f"https://fmteam.fr/api/download/{manga_current_name}/fr/ch/{chapter_number_1}/sub/{chapter_number_2}")
            else:
                lien_chapitre = str(f"https://fmteam.fr/api/download/{manga_current_name}/fr/ch/{chapter_number}")
            try:
                response_url = requests.get(lien_chapitre) # Effectuer une requête HTTP sur l'URL donnée
                response = fmteam_download(response_url, nom_fichier)
                if response == True:
                    print(f"\nTéléchargement {current_download} terminé.\n")                                       ##### Track activity
                else:
                    print(f"\nTéléchargement {current_download} impossible OU dossier déjà existant.\n")                                    ##### Track activity
            except:
                print(f"REQUEST ERROR INFOS : {selected_website} | {manga_current_name} | {chapter_number}")              ##### Track activity

        else:
            None     ############ Add another method for another website here ###########
        


    def perform_download():
        global current_download
        global total_downloads
        global Download_state
        global manga_current_name

        Download()
        current_download += 1
        progress = int((current_download / total_downloads) * 100)
        progressbar["value"] = progress
        percentage_label["text"] = f"{progress}%"
        window.update_idletasks()

        if current_download < total_downloads:
            window.after(2000, perform_download)  # Passer au prochain téléchargement après 2 s
        else:
            progressbar.place_forget()
            percentage_label.place_forget()
            messagebox.showinfo("Information", "Successfull Pandaload 🐼")
            Hide_DownloadBox() # cacher la barre d'infos après 2 secondes
            button_1.configure(state="normal")  # Réactiver le bouton de téléchargement
            Download_state = False
            
    def Download_settings():
        global Download_state
        global nom_fichier

        canvas.itemconfigure(image_1, state=tk.NORMAL)
        Download_state = True
        button_1.configure(state="disabled")  # Désactiver le bouton de téléchargement
        progressbar.place(x=800.0, y=520.0) 
        percentage_label.place(x=830.0, y=545.0) 
        perform_download()

    if select_all_var.get() == 1 and All_chapters_len != 0:
        total_downloads = All_chapters_len
        nom_fichier = script_directory / manga_current_name
        if not os.path.exists(nom_fichier):
            os.makedirs(nom_fichier)
        Download_settings()
    elif total_downloads == 0:
        print('Aucun élément sélectionné')                                              ##### Track activity
    else:
        nom_fichier = script_directory / manga_current_name
        if not os.path.exists(nom_fichier):
            os.makedirs(nom_fichier)
        Download_settings()
    
# Sélectionner tous les chapitres / Volumes d'un manga en cliquant sur la CheckBox
def select_all():
    global chapitres
    global All_chapters_len
    global chapters_current_selected
    global manga_current_name
    global total_downloads

    if select_all_var.get() == 1:
        chapters_box.select_set(0, tk.END)  # Sélectionner tous les éléments de la ListBox
        chapters = chapitres[manga_current_name]
        chapters_current_selected = chapters
        print(chapters_current_selected)    # Afficher tous les chapitres sélectionnés               ##### Track activity
        All_chapters_len = len(chapters_current_selected)
        total_downloads = All_chapters_len
        canvas.itemconfigure(Chapter_selected, text=f'{All_chapters_len} selected')
    else:
        chapters_box.selection_clear(0, tk.END)  # Désélectionner tous les éléments de la ListBox
        chapters_current_selected = [] # réinitialiser la sélection des chapitres
        print(chapters_current_selected)    # Afficher tous les chapitres sélectionnés               ##### Track activity
        canvas.itemconfigure(Chapter_selected, text=f'0 selected')

# Update les résultats de recherche de la SearchBar dans la Manga Name List
def update_results(event):
    keyword = entry_1.get()
    cleaned_datas = datas['name'].fillna('')  # Remplacer les valeurs manquantes par une chaîne vide
    results = cleaned_datas[cleaned_datas.str.contains(keyword, case=False)]
    result_list = results.tolist()  # Convertir les résultats en liste
    result_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste
    for result in result_list:
        result_box.insert(tk.END, result)  # Insérer chaque résultat dans la liste

# Actions lorsqu'un manga est sélectionné
def on_mangas_select(event):
    global manga_current_name

    selected_indices = result_box.curselection()  # Récupérer les indices des éléments sélectionnés
    selected_items = [result_box.get(index) for index in selected_indices]  # Récupérer les éléments sélectionnés
    if selected_items:
        print(selected_items)                                                       ##### Track activity
        manga_name = selected_items[0]
        manga_current_name = manga_name
        try:
            update_chapters(manga_name)
            if len(manga_name) > 15:
                truncated_text = manga_name[:15] + "..."
                canvas.itemconfigure(Manga_selected, text=truncated_text)
            else:
                canvas.itemconfigure(Manga_selected, text=manga_name)
        except:
            print("aucun manga sélectionné")                                            ##### Track activity

# Update les résultats dans la Chapter List lorqu'un manga est sélectionné
def update_chapters(manga_name):
    global chapitres
    global All_chapters_len

    if manga_name in chapitres:
        chapters = chapitres[manga_name]
        chapters_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste déroulante
        All_chapters_len = len(chapters) # Récupérer le nombre total de chapitres du manga sélectionné
        for chapter in chapters:
            chapters_box.insert(tk.END, chapter)  # Insérer chaque chapitre dans la liste déroulante
        if select_all_var.get() == 1:
            select_all()

# Actions lorsque des chapitres sont sélectionnés
def on_chapters_select(event):
    global total_downloads
    global chapters_current_selected
    
    selected_chapters = chapters_box.curselection()  # Récupérer les indices des chapitres sélectionnés
    selected_items = [chapters_box.get(index) for index in selected_chapters]  # Récupérer les chapitres sélectionnés
    chapters_current_selected = selected_items
    print(selected_items)                                                                       ##### Track activity
    total_downloads = len(selected_items)
    canvas.itemconfigure(Chapter_selected, text=f'{total_downloads} selected')

#### Évènements lorsque la souris Entre/Sort d'un bouton ###
def Download_enter(event):
    global Download_state
    if Download_state == True:
        None
    else:
        button_1.configure(image=button_download_2)

def Download_leave(event):
    button_1.configure(image=button_download_1)

def Update_enter(event):
    button_2.configure(image=button_update_2)

def Update_leave(event):
    button_2.configure(image=button_update_1)
############################################################################################################################################################

Name_App = PhotoImage(
    file=relative_to_assets("Name_App.png"))                                                   ### logo du nom de l'appli
image_9 = canvas.create_image(
    481.0,
    65.0,
    image=Name_App
)

Logo_App = PhotoImage(
    file=relative_to_assets("Logo_App.png"))                                                   ### logo d'appli 🐼
image_10 = canvas.create_image(
    85.0,
    65.0,
    image=Logo_App
)

SearchBar_background = PhotoImage(
    file=relative_to_assets("SearchBar_background.png"))                                       ### Background de la barre de recherche
image_7 = canvas.create_image(
    495.0,
    209.0,
    image=SearchBar_background
)

SearchBar_frontground = PhotoImage(
    file=relative_to_assets("SearchBar_frontground.png"))                                      ### Frontground de la barre de recherche
image_8 = canvas.create_image(
    511.0,
    202.0,
    image=SearchBar_frontground
)

##########################################################################################    SearchBar
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))   # Défini le rectangle d'entrée de la SearchBar
entry_bg_1 = canvas.create_image(
    510.5,
    204.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=376.0,
    y=195.0,
    width=269.0,
    height=16.0
)
##########################################################################################  Choix déroulant site de scrapping

canvas.create_text(
    413.0,
    150.0,
    anchor="nw",
    text="🌐",                                                                    ### 🌐
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

# Liste déroulante pour le choix du site
website_list_var = StringVar(window)
website_list_var.set(selected_website)  # Valeur par défaut

# Langues par défaut ( possibilité d'ajouter d'autres langues )
website_menu = OptionMenu(
    window,
    website_list_var,
    "scantrad-vf",
    "lelscans.net",
    "fmteam.fr"
)
website_menu.place(
    x=440.0,
    y=150.0
)
website_menu.configure(
    bg="#FFFFFF"
)
# Associer la fonction au changement de site en utilisant trace_add()
website_list_var.trace_add("write", Update_website)

##########################################################################################

Chapters_list_Box = PhotoImage(
    file=relative_to_assets("Chapters_list_Box.png"))                                           ### Zone d'infos sur les chapitres disponibles
image_5 = canvas.create_image(
    588.8148193359375,
    392.142578125,
    image=Chapters_list_Box
)

Manga_name_listBox = PhotoImage(
    file=relative_to_assets("Manga_name_listBox.png"))                                          ### Zone d'infos sur les mangas disponibles
image_6 = canvas.create_image(
    382.6719970703125,
    392.142578125,
    image=Manga_name_listBox
)

##########################################################################################      Manga Name Box
canvas.create_text(
    331.0,
    269.0,
    anchor="nw",
    text="Manga Name",                                                                          ### Manga Name (Text)
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

# Créer une scrollbar pour la liste des noms de mangas
result_scrollbar = tk.Scrollbar(window)
result_box = tk.Listbox(window, selectmode=tk.SINGLE)                                           # liste pour afficher les noms de mangas
result_box.place(x=306.0, 
                 y=300.0, 
                 width=150, 
                 height=190)

result_scrollbar.config(command=result_box.yview)                               # Lié l'élément de la scrollbar à la liste de noms de mangas
result_scrollbar.place(x=265, y=300, height=190)                                      # Barre de défilement
result_box.config(yscrollcommand=result_scrollbar.set, bd=0)                          # Liste
##########################################################################################      Chapter Available Box
canvas.create_text(
    525.0,
    269.0,
    anchor="nw",
    text="Chapter / Volume",                                                                    ### Chapter / Volume (Text)
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

# Créer une scrollbar pour la liste des chapitres
chapters_scrollbar = tk.Scrollbar(window)
chapters_box = tk.Listbox(window, selectmode=tk.MULTIPLE)                                       # liste déroulante pour afficher les chapitres
chapters_box.place(x=535.0, 
                 y=300.0, 
                 width=100, 
                 height=190)

chapters_scrollbar.config(command=chapters_box.yview)                             # Lié l'élément de la scrollbar à la liste de chapitres
chapters_scrollbar.place(x=685, y=300, height=190)                                      # Barre de défilement 
chapters_box.config(yscrollcommand=chapters_scrollbar.set, bd=0)                        # Liste 

##########################################################################################


##########################################################################################      Association des évènements
# Associer l'événement '<KeyRelease>' à la fonction de mise à jour des résultats
entry_1.bind('<KeyRelease>', update_results)

# Associer l'événement '<ListboxSelect>' à la fonction de capture de la sélection
result_box.bind('<<ListboxSelect>>', on_mangas_select)

# Associer l'événement '<ListboxSelect>' à la fonction de capture de la sélection des chapitres
chapters_box.bind('<<ListboxSelect>>', on_chapters_select)
##########################################################################################


############################################### Informations de téléchargement ##########################################    
Info_download = PhotoImage(
    file=relative_to_assets("Info_download.png"))                                              
image_1 = canvas.create_image(
    843.0,
    575.0,
    image=Info_download,
    state=tk.HIDDEN  # Cacher l'image dès le début
)

progressbar = ttk.Progressbar(window, mode="determinate")       # Création de la barre de progression
percentage_label = tk.Label(window, text="0%", bg="white")                  # Création du label pour afficher le pourcentage

#########################################################################################################################

select_all_var = tk.IntVar() # Création d'une variable entière pour suivre l'état de la Checkbox ( 0 / 1 )
# Création de la checkBox pour sélectionner tous les chapitres d'un Manga
Check_box = tk.Checkbutton(window, text="Select All", variable=select_all_var, command=select_all,bg="white")                     ### Checkbox
Check_box.place(
    x=547.0,
    y=525.0)

chapters_info_box = PhotoImage(
    file=relative_to_assets("Chapters_info.png"))                                               ### Zone d'infos sur les chapitres disponibles
image_3 = canvas.create_image(
    588.0,
    584.0,
    image=chapters_info_box
)

Manga_name_info_box = PhotoImage(
    file=relative_to_assets("Manga_name_info.png"))                                             ### Zone d'infos sur les mangas disponibles
image_4 = canvas.create_image(
    381.0,
    584.0,
    image=Manga_name_info_box
)

Manga_selected = canvas.create_text(
    305.0,
    570.0,
    anchor="nw",
    text="",                                                                                 ### Manga Sélectionné
    fill="#6B0000",
    font=("Inter", 16 * -1)
)

Chapter_selected = canvas.create_text(
    550.0,
    570.0,
    anchor="nw",
    text="",                                                                                 ### Nombre de Chapitres sélectionnés
    fill="#6B0000",
    font=("Inter", 16 * -1)
)

##########################################################################################    BUTTONS   ############################################################################
button_download_2 = PhotoImage(file=relative_to_assets("Download_2.png"))
button_download_1 = PhotoImage(file=relative_to_assets("Download_1.png"))                  
button_1 = Button(
    image=button_download_1,
    borderwidth=0,
    highlightthickness=0,
    command=show_Download_info,
    relief="flat",
    cursor="hand2"
)
button_1.place(
    x=801.0,
    y=584.0,
    width=95.0,
    height=93
)
button_1.bind("<Enter>", Download_enter)  # Lorsque la souris entre dans la zone du bouton
button_1.bind("<Leave>", Download_leave)   # Lorsque la souris quitte la zone du bouton
############################################
button_update_2 = PhotoImage(file=relative_to_assets("Update_2.png"))
button_update_1 = PhotoImage(file=relative_to_assets("Update_1.png"))
button_2 = Button(
    image=button_update_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_update clicked"),                                 ##### Track activity
    relief="flat",
    cursor="hand2 "
)
button_2.place(
    x=664.0,
    y=57.0,
    width=41.0,
    height=44.0
)
button_2.bind("<Enter>", Update_enter)  # Lorsque la souris entre dans la zone du bouton
button_2.bind("<Leave>", Update_leave)   # Lorsque la souris quitte la zone du bouton
######################################################################################################################################################################################

# Action à exécuter lors de la fermeture de la fenêtre
window.protocol("WM_DELETE_WINDOW", on_closing)

window.resizable(False, False)
window.mainloop()