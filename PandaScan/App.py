#------------------------------------------------------------------------------------------------------------
'''
██████╗  █████╗ ███╗   ██╗██████╗  █████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗    
██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║    
██████╔╝███████║██╔██╗ ██║██║  ██║███████║    ███████╗██║     ███████║██╔██╗ ██║    
██╔═══╝ ██╔══██║██║╚██╗██║██║  ██║██╔══██║    ╚════██║██║     ██╔══██║██║╚██╗██║    
██║     ██║  ██║██║ ╚████║██████╔╝██║  ██║    ███████║╚██████╗██║  ██║██║ ╚████║    
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ BETA                                                                                                           
'''
# ------------------------------------------------------------------------------------------------------------
# Welcome to PandaScan ( BETA ) 🐼 | @2023 by CAprogs
# This project aims to download mangas scans from a website by simply selecting the manga and chapters.
# Chromedriver is required to use the app. Please follow the 'Installation Guide'.
# You are now able to change Settings directly in App. ( Need to restart App )
#    ° Select your Update mode || Choose 'manual', 'auto' or anything else ( desable the Update Function ) 
#    ° Select where to save your files after a download 
#    ° If you recently Updated your DB, check changes in the changelog.txt file generated. || websites > choose a website > changelog > changelog.txt
# Please note that some websites may provide empty chapters in their files.
# If this project helped you, please consider giving it a ⭐️ on Github.🫶
# Credits: @Tkinter-designer by ParthJadhav 
# ------------------------------------------------------------------------------------------------------------

# To-Do-List :
# Apres un update reload l'application
# Apres une modif des settings reload l'application
# Rendre les paramètres de l'application réglables directement dans l'app.
# Améliorer la vitesse de téléchargement en utilisant des Threads cpu ou un processus de parallélisation des tâches
# Traquer les progressions des téléchargements et des mises à jour ( fmteam, scantrad-vf, lelscans)
# Changer la barre de progression avec le module tqdm ( tester son implémentation pour track le téléchargement dans le terminal )
# Explorer le multiprocessing avec MPIRE ( Github )
# Utisation d'assertions pour le debogage ( assert )
# Mettre à jour la docu Github.
# Réécrire tous les commentaires en anglais + suppression des commentaires inutiles.

# Importation des bibliothèques utiles
import os
import tkinter as tk
import requests
import sqlite3
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, StringVar, OptionMenu
from pathlib import Path
from tkinter import messagebox
from Download import chapter_transform, Initialize_Download
from Update import Manual_Update,Auto_Update,script_directory
from Selenium_config import driver,config

################################    Variables Globales   ############################################
All_chapters_len = 0    #  stocker le nombre de chapitres total d'un manga sélectionné
total_downloads = 0     #  stocker le nombre de téléchargements de Chapitres à effectuer
current_download = 0    #  variable d'incrémentation du nombre de téléchargements
manga_current_name = '' #  stocker le nom du manga sélectionné
chapters_current_selected = [] # stocker la liste des chapitres sélectionnés
Download_state = False # Etat du bouton Download
nom_fichier = '' # Chemin vers le fichier du manga à télécharger
selected_website = "scantrad-vf" # Site de scrapping par défaut
#################################################################################################

# chemin relatif vers les assets de l'application
assets_directory = script_directory / "assets"

# Charger les datas de la base de données SQLite
try:
    conn = sqlite3.connect(f'{script_directory}/websites/Pan_datas.db')
    cursor = conn.cursor()
    print("\nDatas Loaded ✅")                                                                      ##### Track activity
except:
     messagebox.showinfo("Error [🔄📊]","😵‍💫 Oups, Some datas are missing. 🚨")                       ##### Track activity
     exit()

#################################################################################################

def check_internet_connection():
    """Vérifier si l'utilisateur est connecté à Internet

    Returns:
        _type_: True si l'utilisateur est connecté à Internet, False sinon
    """    
    try:
        # Effectuer une requête vers un site web quelconque
        response = requests.get("https://www.google.com")
        # Si la réponse est valide (code 200)
        if response.status_code == 200:
            print("\nConnected to Internet ✅\n")                                                          ##### Track activity
            return True
        else:
            return False
    except requests.ConnectionError:
        return False
    except Exception as e:
        return False

########################################################    MAIN FUNCTION    ############################################################
def main():
    """Fonction principale de l'application

    Returns:
        _type_: None
    """    
    if not check_internet_connection():
        messagebox.showinfo("Error [🛜]","😵‍💫 Oups, no internet connection detected ❗️")
        return
    
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

    #########################################################   FUNCTIONS    ########################################################
    def relative_to_assets(path: str) -> Path:
        """Get the relative path to the assets folder."""        
        return assets_directory / Path(path)

    def on_closing():
        """Action à effectuer à la fermeture de l'application
        """
        if driver:                                      # Si le navigateur est ouvert
            driver.quit()                               # Fermer le navigateur
        conn.close()                                    # Arrêter la connexion à la base de données
        window.destroy()                                # Fermeture de la fenêtre tkinter
        print("\nApp closed 👋.\n")                     # Afficher le message de deconnexion      ##### Track activity

    def Reinitialize_page():
        """Reinitialise toute la page ( Searchbar, ChapterList, ChapterBox, MangaBox, MangaList, manga_current_name )
        """
        global manga_current_name

        entry_1.delete(0, tk.END)  # Efface le contenu de la SearchBar                                              
        canvas.itemconfigure(Chapter_selected, text='') # Effacer le contenu précédent de la ChapterBox
        canvas.itemconfigure(Manga_selected, text='') # Effacer le contenu précédent de la MangaBox
        manga_current_name = '' # Effacer le contenu précédent du manga sélectionné
        result_box.delete(0, tk.END)  # Effacer le contenu précédent de la mangas list
        chapters_box.delete(0, tk.END)  # Effacer le contenu précédent de la chapters list

    def Switch_Website(*args):
        """Changer de site de scrapping
        """    
        global selected_website

        selected_item = website_list_var.get()
        selected_website = selected_item
        print(f"\nWebsite : {selected_item}")                                           ##### Track activity
        Reinitialize_page()

    def select_all():
        """Sélectionner tous les chapitres / Volumes d'un manga en cliquant sur la CheckBox
        """    
        global total_downloads,manga_current_name,chapters_current_selected
    
        if select_all_var.get() == 1:
            chapters_box.select_set(0, tk.END)  # Sélectionner tous les éléments de la ChapterBox
            query = "SELECT Chapitres FROM Chapitres WHERE NomSite = ? AND NomManga = ?"
            cursor.execute(query, (selected_website, manga_current_name))
            results = cursor.fetchall()
            chapters_current_selected = [chapitre[0] for chapitre in results] # créer une liste composée des chapitres sélectionnés

            print(chapters_current_selected)    # Afficher tous les chapitres sélectionnés               ##### Track activity
            All_chapters_len = len(chapters_current_selected)
            total_downloads = All_chapters_len
            canvas.itemconfigure(Chapter_selected, text=f'{All_chapters_len} selected')
        else:
            chapters_box.selection_clear(0, tk.END)  # Désélectionner tous les éléments de la ListBox
            chapters_current_selected = [] # réinitialiser la sélection des chapitres
            print(chapters_current_selected)    # Afficher tous les chapitres sélectionnés               ##### Track activity
            canvas.itemconfigure(Chapter_selected, text=f'0 selected')

    def update_results(event):
        """Update les résultats de recherche de la SearchBar dans la Manga Name List

        Args:
            event (_type_): L'événement qui déclenche la fonction
        """    
        global selected_website

        keyword = entry_1.get()
        query = f"SELECT NomManga FROM Mangas WHERE NomManga LIKE ? AND NomSite = '{selected_website}'"
        cursor.execute(query, ('%' + keyword + '%',)) # Rechercher les mangas correspondant au mot-clé
        results = cursor.fetchall() # Récupérez les Noms de Mangas correspondant au mot-clé
        result_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste
        # Affichez les résultats dans la MangaBox
        for result in results:
            result_box.insert(tk.END, result[0])  # Insérer chaque MANGA dans la liste déroulante

    def on_mangas_select(event):
        """Actions lorsqu'un manga est sélectionné

        Args:
            event (_type_): L'événement qui déclenche la fonction
        """    
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

    def update_chapters(manga_name):
        """Update les résultats dans la Chapter List lorqu'un manga est sélectionné

        Args:
            manga_name (_type_): Le nom du manga sélectionné
        """    

        # Rechercher tous les chapitres du manga sélectionné
        query = "SELECT Chapitres FROM Chapitres WHERE NomSite = ? AND NomManga = ?"
        cursor.execute(query, (selected_website, manga_name))
        results = cursor.fetchall()  # Récupérer tous les chapitres correspondant au manga sélectionné
        chapters_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste déroulante
        # Afficher les résultats dans la ChapterBox
        for result in results:
            chapters_box.insert(tk.END, result[0])  # Insérer chaque CHAPITRE dans la liste déroulante
        if select_all_var.get() == 1:
            select_all()

    def on_chapters_select(event):
        """Actions lorsque des chapitres sont sélectionnés

        Args:
            event (_type_): L'événement qui déclenche la fonction
        """    
        global chapters_current_selected, total_downloads
        
        selected_chapters = chapters_box.curselection()  # Récupérer les indices des chapitres sélectionnés
        selected_items = [chapters_box.get(index) for index in selected_chapters]  # Récupérer les chapitres sélectionnés
        chapters_current_selected = selected_items
        print(selected_items)                                                                       ##### Track activity
        total_downloads = len(selected_items)
        canvas.itemconfigure(Chapter_selected, text=f'{total_downloads} selected')

    def show_Download_info():
        """Download ou non les éléments sélectionnés
        """    
        global current_download, total_downloads

        # Réinitialiser les variables du téléchargement
        current_download = 0

        def Hide_DownloadBox():
            """Cacher la barre d'infos
            """        
            canvas.itemconfigure(image_1, state=tk.HIDDEN)
        
        def Download():
            """Télécharger les chapitres sélectionnés
            """        
            global selected_website

            chapter_name = chapters_current_selected[current_download]  # Nom du Chapitre
            if os.path.exists(config['Download']['path']): 
                nom_chapitre = nom_fichier + '/' + chapter_name
            else:
                nom_chapitre = nom_fichier / chapter_name
            # Création du Dossier du chapitre correspondant s'il n'existe pas
            chapter_number = chapter_transform(chapter_name, selected_website) # retourne le format adapté pour le site correspondant
            Initialize_Download(selected_website, nom_chapitre, manga_current_name, chapter_number, current_download, chapter_name, nom_fichier, config, cursor)

        def perform_download():
            """Télécharger les chapitres sélectionnés
            """        
            global current_download, Download_state, total_downloads

            Download()
            current_download += 1
            if total_downloads > 1:
                progress = int((current_download / total_downloads) * 100)
                progressbar["value"] = progress
                percentage_label["text"] = f"{progress}%"
                window.update_idletasks()

            if current_download < total_downloads:
                window.after(2000, perform_download)  # Passer au prochain téléchargement après 2 s
            else:
                if total_downloads > 1:
                    progressbar.place_forget()
                    percentage_label.place_forget()
                messagebox.showinfo("Info [ℹ️]", "Successfull Pandaload ✅, Thanks for using PandaScan 🐼")
                Hide_DownloadBox() # cacher la barre d'infos
                button_1.configure(state="normal")  # Réactiver le bouton de téléchargement
                Download_state = False
        
        def Download_settings():
            """Télécharger les chapitres sélectionnés
            """        
            global Download_state, total_downloads

            Download_state = True
            button_1.configure(state="disabled")  # Désactiver le bouton de téléchargement
            if total_downloads > 1: # Si plusieurs chapitres sont sélectionnés on affiche la barre de progression et le pourcentage sinon on ne l'affiche pas
                canvas.itemconfigure(image_1, state=tk.NORMAL)   
                progressbar.place(x=800.0, y=520.0) 
                percentage_label.place(x=830.0, y=545.0) 
            perform_download()

        def Set_Download_Path():
            """ Gérer le chemin de destination des téléchargements
            """        
            global nom_fichier

            if os.path.exists(config['Download']['path']):
                nom_fichier = config['Download']['path'] + '/' + manga_current_name
            else:
                nom_fichier = script_directory / manga_current_name
                if not os.path.exists(nom_fichier):
                    os.makedirs(nom_fichier)
            Download_settings()

        if select_all_var.get() == 1 and All_chapters_len != 0:
            total_downloads = All_chapters_len
            Set_Download_Path()
        elif total_downloads == 0:
            messagebox.showinfo("Info [ℹ️]", "No Chapter Selected 🤕, Try again")
        else:
            Set_Download_Path()
    
    def set_button_color(event,button,button_image):
        """ Action lorsque la souris survole/sort du bouton.

        Args:
            event (_type_): L'événement qui déclenche la fonction
        """
        if Download_state == True:
            None
        else:
            button.configure(image=button_image)

    ############################################################################################################################################################

    #########################################################     ELEMENTS    #########################################################

    # ============================================ Éléments Graphiques principaux de l'App
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

    SearchBar_foreground = PhotoImage(
        file=relative_to_assets("SearchBar_foreground.png"))                                      ### Foreground de la barre de recherche
    image_8 = canvas.create_image(
        511.0,
        202.0,
        image=SearchBar_foreground
    )

    # ============================================ Barre de Recherche des mangas ( SearchBar )
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

    # ============================================ Choix déroulant Website
    canvas.create_text(
        413.0,
        152.0,
        anchor="nw",
        text="🌐",                                                                    ### 🌐
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    # Liste déroulante pour le choix du site
    website_list_var = StringVar(window)
    website_list_var.set(selected_website)  # Valeur par défaut

    # Sites par défaut dans la liste déroulante
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
    website_list_var.trace_add("write", Switch_Website)

    # ============================================ Zone d'affichage des Chapitres ( ChapterBox : Image )

    Chapters_list_Box = PhotoImage(
        file=relative_to_assets("Chapters_list_Box.png"))                                           ### Zone d'infos sur les chapitres disponibles
    image_5 = canvas.create_image(
        588.8148193359375,
        392.142578125,
        image=Chapters_list_Box
    )

    # ============================================ Zone d'affichage des noms de Mangas ( MangaBox : Image )
    Manga_name_listBox = PhotoImage(
        file=relative_to_assets("Manga_name_listBox.png"))                                          ### Zone d'infos sur les mangas disponibles
    image_6 = canvas.create_image(
        382.6719970703125,
        392.142578125,
        image=Manga_name_listBox
    )

    # ============================================ Zone d'affichage des noms de Mangas ( MangaBox : Text et ScrollBar )
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

    # ============================================ Zone d'affichage des Chapitres ( ChapterBox : Text et ScrollBar )
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

    # ============================================  Association des évènements liés à la sélection de mangas & chapitres
    # Associer l'événement '<KeyRelease>' à la fonction de mise à jour des résultats
    entry_1.bind('<KeyRelease>', update_results)

    # Associer l'événement '<ListboxSelect>' à la fonction de capture de la sélection
    result_box.bind('<<ListboxSelect>>', on_mangas_select)

    # Associer l'événement '<ListboxSelect>' à la fonction de capture de la sélection des chapitres
    chapters_box.bind('<<ListboxSelect>>', on_chapters_select)

    # ============================================ Informations au cours d'un téléchargement    ( Download_info )
    Info_download = PhotoImage(
        file=relative_to_assets("Info_download.png"))                                              
    image_1 = canvas.create_image(
        843.0,
        575.0,
        image=Info_download,
        state=tk.HIDDEN  # Cacher l'image au lancement de l'application
    )

    progressbar = ttk.Progressbar(window, mode="determinate")       # Création de la barre de progression
    percentage_label = tk.Label(window, text="0%", bg="white")      # Création du label pour afficher le pourcentage

    # ============================================ Case à cocher pour sélectionner tous les chapitres d'un manga ( Checkbox )
    select_all_var = tk.IntVar() # Création d'une variable entière pour suivre l'état de la Checkbox
    # Création de la checkBox pour sélectionner tous les chapitres d'un Manga
    Check_box = tk.Checkbutton(window, text="Select All", variable=select_all_var, command=select_all,bg="white")                     ### Checkbox
    Check_box.place(
        x=547.0,
        y=525.0)

    # ============================================ Zone d'infos sur le nombre de chapitres sélectionnés ( Chapters_info Box )
    chapters_info_box = PhotoImage(
        file=relative_to_assets("Chapters_info.png"))
    image_3 = canvas.create_image(
        588.0,
        584.0,
        image=chapters_info_box
    )

    Chapter_selected = canvas.create_text(
        550.0,
        570.0,
        anchor="nw",
        text="",                                                                                 ### Nombre de Chapitres sélectionnés
        fill="#6B0000",
        font=("Inter", 16 * -1)
    )

    # ============================================ Zone d'infos sur le nom du manga sélectionné ( Manga_info Box )
    Manga_name_info_box = PhotoImage(
        file=relative_to_assets("Manga_name_info.png"))
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

    #################################################################   BUTTONS   ############################################################################

    # ============================================  DOWNLOAD
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
    button_1.bind("<Enter>", lambda event:set_button_color(event, button_1, button_download_2))
    button_1.bind("<Leave>", lambda event:set_button_color(event, button_1, button_download_1))

    # ============================================  SETTINGS
    button_settings_2 = PhotoImage(file=relative_to_assets("Settings_2.png"))
    button_settings_1 = PhotoImage(file=relative_to_assets("Settings_1.png"))                  
    button_3 = Button(
        image=button_settings_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:print("settings clicked"),
        relief="flat",
        cursor="hand2"
    )
    button_3.place(
        x=830.0,
        y=25.0,
        width=108.0,
        height=40
    )
    button_3.bind("<Enter>", lambda event:set_button_color(event, button_3, button_settings_2))
    button_3.bind("<Leave>", lambda event:set_button_color(event, button_3, button_settings_1))

    # ============================================  UPDATE
    button_update_2 = PhotoImage(file=relative_to_assets("Update_2.png"))
    button_update_1 = PhotoImage(file=relative_to_assets("Update_1.png"))
    button_2 = Button(
        image=button_update_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        cursor="hand2"
    )
    button_2.place(
        x=664.0,
        y=57.0,
        width=41.0,
        height=44.0
    )

    if config['Update']['mode'].lower() == "auto":                                                                  # Si mode = auto, on active l'auto update
        window.withdraw()  # Cacher l'application pendant la mise à jour automatique
        button_2.config(state=tk.DISABLED, cursor="arrow")                                                          # On désactive le bouton Update
        Auto_Update(script_directory,config,conn,cursor)
        window.deiconify()  # Réafficher l'application après la mise à jour automatique
    elif config['Update']['mode'].lower() == "manual":                                                              # Si mode = manual, on active l'update manuel
        button_2.config(command=lambda: Manual_Update(script_directory,selected_website,config,conn,cursor))
        button_2.bind("<Enter>", lambda event:set_button_color(event, button_2, button_update_2))
        button_2.bind("<Leave>", lambda event:set_button_color(event, button_2, button_update_1))
    else:
        button_2.config(state=tk.DISABLED, cursor="arrow")                                                          # Action si le mode n'est pas reconnu
        driver.quit()                                                                                               # Fermer le navigateur
        print("\n Update Button inactive [set Update to 'manual' or 'auto' in settings] ")                                          ##### Track activity
    
    ######################################################################################################################################################################################

    # Action à exécuter lors de la fermeture de la fenêtre
    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    main()