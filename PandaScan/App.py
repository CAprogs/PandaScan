# ------------------------------------------------------------------------------------------------------------
# Welcome to PandaScan 🐼 | @2023 by CAprogs
# This is an project that aims to download mangas scans from a website by selecting the manga and chapters wished.
# Due to some restrictions , those scans can't be download by an simple request so we tae screenshot of the image and then crop it to the right size.
# Internet access, Chomium ( The Automate ChromeBrowser ) and Ublock ( A Chrome Extension ) are required to use this Software.
# The Download Time depends on the number of Chapters to download and their Number of pages.
# An Update button is available so your manga list can be up to date if there's new manga chapters availables ( Not available Yet )
# Credits: @Tkinter Designer by ParthJadhav 
# ------------------------------------------------------------------------------------------------------------

# Importation des bibliothèques utiles
import os
import pandas as pd
import yaml
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from tkinter import messagebox

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

######################################################################    FONCTIONS  & CLASSES  ######################################################################
# Importation des éléments graphique
def relative_to_assets(path: str) -> Path:
    return assets_directory / Path(path)

def show_Download_info():
    canvas.itemconfigure(image_1, state=tk.NORMAL)

def update_results(event):
    keyword = entry_1.get()
    cleaned_datas = datas['name'].fillna('')  # Remplacer les valeurs manquantes par une chaîne vide
    results = cleaned_datas[cleaned_datas.str.contains(keyword, case=False)]
    result_list = results.tolist()  # Convertir les résultats en liste
    result_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste
    for result in result_list:
        result_box.insert(tk.END, result)  # Insérer chaque résultat dans la liste

def on_mangas_select(event):
    selected_indices = result_box.curselection()  # Récupérer les indices des éléments sélectionnés
    selected_items = [result_box.get(index) for index in selected_indices]  # Récupérer les éléments sélectionnés
    if not selected_items:
        print("liste vide")
    else:
        print(selected_items)
        manga_name = selected_items[0]
        try:
            update_chapters(manga_name)
            if len(manga_name) > 15:
                truncated_text = manga_name[:15] + "..."
                canvas.itemconfigure(Manga_selected, text=truncated_text)
            else:
                canvas.itemconfigure(Manga_selected, text=manga_name)
        except:
            print("aucun manga sélectionné")

def update_chapters(manga_name):
    global chapitres
    if manga_name in chapitres:
        chapters = chapitres[manga_name]
        chapters_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste déroulante
        for chapter in chapters:
            chapters_box.insert(tk.END, chapter)  # Insérer chaque chapitre dans la liste déroulante

def on_chapters_select(event):
    global selected_chapters
    selected_chapters = chapters_box.curselection()  # Récupérer les indices des chapitres sélectionnés
    selected_items = [chapters_box.get(index) for index in selected_chapters]  # Récupérer les chapitres sélectionnés
    print(selected_items)
    canvas.itemconfigure(Chapter_selected, text=f'{len(selected_items)} selected')

def Download_enter(event):
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

Info_download = PhotoImage(
    file=relative_to_assets("Info_download.png"))                                               ### Informations de téléchargement
image_1 = canvas.create_image(
    843.0,
    575.0,
    image=Info_download
)
canvas.itemconfigure(image_1, state=tk.HIDDEN)

Check_box = PhotoImage(
    file=relative_to_assets("Check_box.png"))                                                   ### Checkbox 
image_2 = canvas.create_image(
    547.0,
    533.0,
    image=Check_box
)

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

window.resizable(False, False)
window.mainloop()