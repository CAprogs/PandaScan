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
# This is an project that aims to download mangas scans from a website by selecting the manga and chapters wished.
# Due to some restrictions , those scans can't be download by an simple request so we take screenshot of the image and then crop it to the right size.
# Internet access, Chomium ( The Automate ChromeBrowser ) and Ublock ( A Chrome Extension ) are required to use this Software.
# The Download Time depends on the number of Chapters to download and their Number of pages.
# An Update button is available so your manga list can be up to date if there's new manga chapters availables ( Not available Yet )
# Credits: @Tkinter Designer by ParthJadhav 
# ------------------------------------------------------------------------------------------------------------

# Importation des bibliothèques utiles
import os
import pandas as pd
import yaml
import re
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from tkinter import messagebox
from tkinter.font import Font
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

# Changer de site pour les mangas
# Réajuster les dimensions des crop de mangas

# Obtenir le chemin absolu du répertoire contenant le script
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# chemin relatif vers le dossier "frame0"
assets_directory = script_directory / "frame0"
mangas_path = script_directory / "datas/mangas.csv"
chapters_path = script_directory / "datas/mangas_chapters.yml"

# Chargement des datas
with open(chapters_path, 'r') as file:
        chapitres = yaml.safe_load(file)
datas = pd.read_csv(mangas_path)

################################ Variables Globales ############################################
All_chapters_len = 0    #  stocker le nombre de chapitres total d'un manga sélectionné
total_downloads = 0     #  stocker le nombre de téléchargements de Chapitres à effectuer
current_download = 0    #  variable d'incrémentation du nombre de téléchargements
manga_current_name = '' #  stocker le nom du manga sélectionné
chapters_current_selected = [] # stocker la liste des chapitres sélectionnés
Download_state = False # Etat du bouton Download
nom_fichier = '' # Chemin vers le fichier du manga à télécharger
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

# #====================================================== Configuration de Selenium pour utiliser Chrome ================================================================
# Chemin vers le profil Chrome
chrome_profile_path = '/Users/charles-albert/Library/Application Support/Google/Chrome/Default'
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + chrome_profile_path) # Ajout du profil Chrome
user_agent_cookies = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Extraire le User-Agent et les cookies du format JSON
new_user_agent = user_agent_cookies["user-agent"]

# Utiliser les options du navigateur pour modifier le User-Agent
options.add_argument(f"user-agent={new_user_agent}")

# Instancier le navigateur avec les options configurées
driver = webdriver.Chrome(options=options)
driver.maximize_window() # Ouvrir le navigateur en full size
# =======================================================================================================================================================================

######################################################################    FONCTIONS  & CLASSES  ######################################################################
# Importation des éléments graphique
def relative_to_assets(path: str) -> Path:
    return assets_directory / Path(path)

# Action à effectuer à la fermeture de l'application
def on_closing():
    driver.quit() # Fermeture du navigateur
    window.destroy() # Fermeture de la fenêtre tkinter

# Mettre à jour les chapitres et mangas disponibles
def Update_chapters():  
    None

# Ajouter manuellement des mangas à la liste des mangas disponibles ( ajouter un bouton +)
def Add_mangas_to_list():  
    None

# Fonction pour attribuer le bon format au chapitre / volume
def chapter_or_volume(chapter_name):
    if 'chapitre' in chapter_name:
        result = chapter_name.replace('chapitre ','')
    else:
        result = chapter_name.replace(' ','-')
    return result

# Fonction pour crop l'image
def crop(path_image,size):
    # Récupérer l'image capturée
    image = Image.open(path_image)
    # Dimensions de l'image initiale
    initial_width = size['width'] # Largeur initiale image
    initial_height = size['height'] # Hauteur initiale image
    # Dimensions du screenshot
    screen_width = image.width # Largeur screenshot
    screen_height = image.height # Hauteur screenshot
    # Calculer les coordonnées de recadrage
    x = (screen_width - initial_width) // 2
    y = (screen_height - initial_height) // 2
    a = 25 # Nbre de pixels à ajuster pour la bonne taille
    b = 80 # Nbre de pixels à ajuster pour la bonne taille
    if initial_width > initial_height: # Si l'image est en mode paysage
        # Recadrer l'image en ajustant pour conserver la largeur initiale
        x = ( x // 2 ) + b
        image = image.crop((x,0,screen_width - x,screen_height))
    else:
        # Recadrer l'image pour ne conserver que l'élément souhaité
        image = image.crop((x-a, y-a, x + initial_width+a, y + initial_height+a))
    # Enregistrer l'image recadrée
    image.save(path_image)

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

    def Download():
        global chapters_current_selected
        global manga_current_name
        global current_download
        global nom_fichier

        chapter_name = chapters_current_selected[current_download]  # Nom du Chapitre
        nom_chapitre = nom_fichier / chapter_name
        # Création du Dossier du chapitre correspondant s'il n'existe pas ***
        if not os.path.exists(nom_chapitre):
            os.makedirs(nom_chapitre)
            chapter_number = chapter_or_volume(chapter_name)
            page = 1 # Page de départ
            lien_chapitre = str(f'https://www.japscan.lol/lecture-en-ligne/{manga_current_name}/{chapter_number}/{page}.html')  # Lien du chapitre
            driver.get(lien_chapitre) # Accès à la page avec Selenium
            soup = BeautifulSoup(driver.page_source, 'html.parser') # Transformation de la page pour analyse
            # récupération du nombre de pages du chapitre
            try:
                element = driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/p[6]') # chemin vers l'élément qui contient le nombre de pages (div 6)
            except:
                try:
                    element = driver.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/p[5]') # chemin vers l'élément qui contient le nombre de pages (div 5)            
                except:
                    print("Pas d'informations trouvées.")
                    return
            element_nombre_pages = element.text.strip() # conversion en string
            resultat = re.search(r'\d+', element_nombre_pages) # Utiliser une expression régulière pour extraire le chiffre
            if resultat: # Si on trouve le nombre de pages, on le récupère
                nombre_pages = int(resultat.group(0))
                print(f"""\n Téléchargement en cours ...
                    {chapter_name}
                    {nombre_pages} pages """)
                # Rechercher l'image => Faire un screenshot => Redimensionner l'image => la sauvegarder
                while page <= nombre_pages:
                    image_element = soup.find('div', id='single-reader') # Obtention de la balise contenant l'URL de l'image
                    image_url = image_element.find('img', class_='img-fluid')['src'] # Obtention de l'URL de l'image
                    element = driver.find_element_by_xpath('//*[@id="single-reader"]/img') # Trouver l'élément souhaité sur la page à partir de l'URL de l'image
                    size = element.size
                    driver.get(image_url)
                    # chemin de sauvegarde de l'image
                    path_image = f"{nom_chapitre}/{page}.png"
                    # prendre le screenshot de la page entière
                    driver.save_screenshot(path_image)    
                    crop(path_image,size) # Crop l'image aux bonnes dimensions et la sauvegarder
                    print(f"Page {page} téléchargée.")
                    # Accès à la page suivante
                    page += 1
                    if page > nombre_pages:
                        break
                    else:
                        lien_chapitre=str(f'https://www.japscan.lol/lecture-en-ligne/{manga_current_name}/{chapter_number}/{page}.html')
                        driver.get(lien_chapitre)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Analyse de la nouvelle page
            else:
                print("Aucun chiffre trouvé.")
                return

    def perform_download():                                                                 # Modifier à la fin du programme pour le vrai téléchargement
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
        print('Aucun élément sélectionné')
    else:
        nom_fichier = script_directory / manga_current_name
        if not os.path.exists(nom_fichier):
            os.makedirs(nom_fichier)
        Download_settings()
    
# Sélectionner tous les chapitres / Volumes d'un manga en cliquant sur la CheckBox
def select_all():
    global All_chapters_len

    if select_all_var.get() == 1:
        chapters_box.select_set(0, tk.END)  # Sélectionner tous les éléments de la ListBox
        canvas.itemconfigure(Chapter_selected, text=f'{All_chapters_len} selected')
    else:
        chapters_box.selection_clear(0, tk.END)  # Désélectionner tous les éléments de la ListBox
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
    if not selected_items:
        print("liste vide")
    else:
        print(selected_items)
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
            print("aucun manga sélectionné")

# Update les résultats dans la Chapter List lorqu'un manga est sélectionné
def update_chapters(manga_name):
    global chapitres
    global All_chapters_len
    global chapters_current_selected

    if manga_name in chapitres:
        chapters = chapitres[manga_name]
        chapters_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste déroulante
        for chapter in chapters:
            chapters_box.insert(tk.END, chapter)  # Insérer chaque chapitre dans la liste déroulante
        All_chapters_len = len(chapters) # Récupérer le nombre total de chapitres du manga sélectionné
        if select_all_var.get() == 1:
            select_all()
            chapters_current_selected = chapters

# Actions lorsque des chapitres sont sélectionnés
def on_chapters_select(event):
    global selected_chapters
    global total_downloads
    global chapters_current_selected

    selected_chapters = chapters_box.curselection()  # Récupérer les indices des chapitres sélectionnés
    selected_items = [chapters_box.get(index) for index in selected_chapters]  # Récupérer les chapitres sélectionnés
    chapters_current_selected = selected_items
    print(selected_items)
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
    command=lambda: print("button_update clicked"),
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
