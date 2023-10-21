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
# You are now able to change Settings directly in App. ( you may need to restart App to apply changes )
#    ° Select your Update mode || Choose 'manual', 'auto' or anything else ( desable the Update Function ) 
#    ° Select where to save your files after a download 
#    ° If you recently Updated your DB, check changes in the changelog.txt file generated. || websites > choose a website > changelog > changelog.txt
# Please note that some websites may provide empty chapters in their files.
# If this project helped you, please consider giving it a ⭐️ on Github.🫶
# Credits: @Tkinter-designer by ParthJadhav 
# ------------------------------------------------------------------------------------------------------------

# To-Do-List :
# Implémenter un journal d'application
# Message d'erreur lorqu'un téléchargeemnt est interrompu ou se passe mal
# Nettoyer le code et les importations inutiles ( fichiers __init__.py )
# Apres un update reload l'application
# Apres une modif des settings reload l'application
# Améliorer la vitesse de téléchargement en utilisant des Threads cpu ou un processus de parallélisation des tâches
# Traquer le temps des téléchargements et des mises à jour
# Explorer le multiprocessing avec MPIRE ( Github )
# Utisation d'assertions pour le debogage ( assert ? gestion des erreurs avec Try/except ? )
# Mettre à jour la docu Github.
# Réécrire tous les commentaires en anglais + suppression des commentaires inutiles.

import requests
import sqlite3
from tkinter import messagebox
from Update import script_directory

################################    Variables Globales   ############################################
All_chapters_len = 0                        #  stocker le nombre de chapitres total d'un manga sélectionné
total_downloads = 0                         #  stocker le nombre de téléchargements de Chapitres à effectuer
current_download = 0                        #  variable d'incrémentation du nombre de téléchargements
manga_current_name = ''                     #  stocker le nom du manga sélectionné
chapters_current_selected = []              # stocker la liste des chapitres sélectionnés
Download_state = False                      # Etat du bouton Download
nom_fichier = ''                            # Chemin vers le fichier du manga à télécharger
websites = ["scantrad-vf", "lelscans.net", "fmteam.fr"] # Les sites disponibles
selected_website = websites[0]                          # Site sélectionné par défaut
color_1 = "#FFFFFF"                                     # blanc
color_2 = "#6B0000"                                     # bordeaux
color_3 = "#000716"                                     # noir
police_1 = ("Inter", 15 * -1)
police_2 = ("Inter", 16 * -1)     
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
    except Exception:
        return False

########################################################    MAIN FUNCTION    ############################################################
def main():
    """Fonction principale de l'application

    Returns:
        _type_: None
    """ 
    import os
    import tkinter as tk
    from tkinter import ttk
    from tkinter import Tk, Canvas, Button, PhotoImage, StringVar, OptionMenu
    from pathlib import Path
    from Download import chapter_transform, Initialize_Download
    from Update import Manual_Update,Auto_Update
    from Settings import show_settings,inactive_cursor,active_cursor
    from Selenium_config import driver,config
       
    if not check_internet_connection():
        messagebox.showinfo("Error [🛜]","😵‍💫 Oups, no internet connection detected ❗️")
        return print("Exiting App ..\n")                                                                 ##### Track activity

    print("App successfully launched ✅\n")                                                              ##### Track activity

    # Initialiser la fenêtre Tkinter
    window = Tk()

    # Donner un nom à la fenêtre
    window.title("PandaScan 🐼")

    # Paramètres par défaut de la fenêtre
    window.geometry("962x686")
    window.configure(bg = color_1)
    canvas = Canvas(
        window,
        bg = color_1,
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

        manga_current_name = '' # Effacer le contenu précédent du manga sélectionné

        entry_1.delete(0, tk.END)  # Efface le contenu de la SearchBar                                              
        canvas.itemconfigure(Chapter_selected, text='') # Effacer le contenu précédent de la ChapterBox
        canvas.itemconfigure(Manga_selected, text='') # Effacer le contenu précédent de la MangaBox
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

            #print(chapters_current_selected)    # Afficher tous les chapitres sélectionnés               ##### Track activity
            All_chapters_len = len(chapters_current_selected)
            total_downloads = All_chapters_len
            canvas.itemconfigure(Chapter_selected, text=f'{All_chapters_len} selected')
        else:
            chapters_box.selection_clear(0, tk.END)  # Désélectionner tous les éléments de la ListBox
            chapters_current_selected = [] # réinitialiser la sélection des chapitres
            #print(chapters_current_selected)    # Afficher tous les chapitres sélectionnés               ##### Track activity
            canvas.itemconfigure(Chapter_selected, text=f'0 selected')

    def update_results(event):
        """Update les résultats de recherche de la SearchBar dans la Manga Name List

        Args:
            event (_type_): L'événement qui déclenche la fonction
        """    
        global selected_website

        keyword = entry_1.get() # Récupérer l'entrée de la searchbar
        keyword = '%' + keyword + '%' 
        query = f"SELECT NomManga FROM Mangas WHERE NomManga LIKE ? AND NomSite = ?" # Requête SQL
        cursor.execute(query, (keyword, selected_website)) # Chercher les correspondances dans la DB
        results = [row[0] for row in cursor.fetchall()] # récupérer les correspondances 
        result_box.delete(0, tk.END)   # Supprimer les anciens résultats s'il y'en avaient
        result_box.insert(tk.END, *results)  # Insérer les nouveaux résultats dans la Manga_list box

    def on_mangas_select(event):
        """Actions lorsqu'un manga est sélectionné

        Args:
            event (_type_): L'événement qui déclenche la fonction
        """    
        global manga_current_name

        selected_indices = result_box.curselection() # récupérer l'indice de l'élément sélectionné
        if selected_indices:
            manga_name = result_box.get(selected_indices[0])    # récupérer le nom du manga
            manga_current_name = manga_name
            try:
                update_chapters(manga_name)
                truncated_text = manga_name[:15] + "..." if len(manga_name) > 15 else manga_name
                canvas.itemconfigure(Manga_selected, text=truncated_text)
            except Exception as e:
                print(f"Erreur lors de la sélection du manga : {e}")

    def update_chapters(manga_name):
        """Update les résultats dans la Chapter List lorqu'un manga est sélectionné

        Args:
            manga_name (_type_): Le nom du manga sélectionné
        """
        global selected_website

        # Rechercher tous les chapitres du manga sélectionné
        query = "SELECT Chapitres FROM Chapitres WHERE NomSite = ? AND NomManga = ?"
        cursor.execute(query, (selected_website, manga_name))
        results = [result[0] for result in cursor.fetchall()]  # Utilisation d'indices
        chapters_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste déroulante

        # Afficher les résultats dans la ChapterBox
        chapters_box.insert(tk.END, *results)  # Utilisation de l'opérateur * pour insérer tous les chapitres

        if select_all_var.get() == 1:
            select_all()

    def on_chapters_select(event):
        """Actions lorsque des chapitres sont sélectionnés

        Args:
            event (_type_): L'événement qui déclenche la fonction
        """    
        global chapters_current_selected, total_downloads
        
        selected_chapters = chapters_box.curselection()     # récupérer les indices des chapitres sélectionnés
        chapters_current_selected = [chapters_box.get(index) for index in selected_chapters]  # récupérer les chapitres sélectionnés
        total_downloads = len(chapters_current_selected)
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
                download_button.configure(state="normal")  # Réactiver le bouton de téléchargement
                Download_state = False
        
        def Download_settings():
            """Télécharger les chapitres sélectionnés
            """        
            global Download_state, total_downloads

            Download_state = True
            download_button.configure(state="disabled")  # Désactiver le bouton de téléchargement
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

    def button_hover(button,button_image_1,button_image_2):
        """ Action lorsque la souris survole/sort du bouton.

        Args:
            button (Any): le bouton qui déclenche la fonction
            button_image_1 (Any): l'image par defaut du bouton
            button_image_2 (Any): l'image lorsque la souris survole le bouton
        """
        def set_button_color(event,button,button_image):
                """ Associer une image à un bouton

                Args:
                    event (Any): L'événement qui déclenche la fonction
                """
                global Download_state

                if Download_state == True:
                    None
                else:
                    button.configure(image=button_image)

        button.bind("<Enter>", lambda event:set_button_color(event, button, button_image_2))
        button.bind("<Leave>", lambda event:set_button_color(event, button, button_image_1))

    ############################################################################################################################################################

    #########################################################     ELEMENTS    #########################################################

    # ============================================ Éléments Graphiques principaux de l'App
    Name_App = tk.PhotoImage(
        file=relative_to_assets("Name_App.png"))                                                   ### logo du nom de l'appli
    image_9 = canvas.create_image(
        481.0,
        65.0,
        image=Name_App
    )

    Logo_App = tk.PhotoImage(
        file=relative_to_assets("Logo_App.png"))                                                   ### logo d'appli 🐼
    image_10 = canvas.create_image(
        85.0,
        65.0,
        image=Logo_App
    )

    SearchBar_background = tk.PhotoImage(
        file=relative_to_assets("SearchBar_background.png"))                                       ### Background de la barre de recherche
    image_7 = canvas.create_image(
        495.0,
        209.0,
        image=SearchBar_background
    )

    SearchBar_foreground = tk.PhotoImage(
        file=relative_to_assets("SearchBar_foreground.png"))                                      ### Foreground de la barre de recherche
    image_8 = canvas.create_image(
        511.0,
        202.0,
        image=SearchBar_foreground
    )

    # ============================================ Barre de Recherche des mangas ( SearchBar )
    entry_image_1 = tk.PhotoImage(
        file=relative_to_assets("entry_1.png"))   # Défini le rectangle d'entrée de la SearchBar
    entry_bg_1 = canvas.create_image(
        510.5,
        204.0,
        image=entry_image_1
    )
    entry_1 = tk.Entry(
        window,
        bd=0,
        bg=color_1,
        fg=color_3,
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
        fill=color_1,
        font=police_1
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
        bg=color_1
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
        fill=color_1,
        font=police_1
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
        fill=color_1,
        font=police_1
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
        fill=color_2,
        font=police_2
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
        fill=color_2,
        font=police_2
    )

    #################################################################   BUTTONS   ############################################################################

    # ============================================  DOWNLOAD
    button_download_2 = PhotoImage(file=relative_to_assets("Download_2.png"))
    button_download_1 = PhotoImage(file=relative_to_assets("Download_1.png"))                  
    download_button = Button(
        window,
        image=button_download_1,
        borderwidth=0,
        highlightthickness=0,
        command=show_Download_info,
        relief="flat",
        cursor=active_cursor
    )
    download_button.place(
        x=801.0,
        y=584.0,
        width=95.0,
        height=93
    )
    button_hover(download_button, button_download_1, button_download_2)

    # ============================================  SETTINGS
    button_settings_2 = PhotoImage(file=relative_to_assets("Settings_2.png"))
    button_settings_1 = PhotoImage(file=relative_to_assets("Settings_1.png"))                  
    settings_button = Button(
        window,
        image=button_settings_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:show_settings(window, config, settings_button),
        relief="flat",
        cursor=active_cursor
    )
    settings_button.place(
        x=830.0,
        y=25.0,
        width=108.0,
        height=40
    )
    button_hover(settings_button, button_settings_1, button_settings_2)

    # ============================================  UPDATE
    button_update_2 = PhotoImage(file=relative_to_assets("Update_2.png"))
    button_update_1 = PhotoImage(file=relative_to_assets("Update_1.png"))
    update_button = Button(
        window,
        image=button_update_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        cursor=active_cursor
    )
    update_button.place(
        x=664.0,
        y=57.0,
        width=41.0,
        height=44.0
    )

    if config['Update']['mode'].lower() == "auto":                                                                  # Si mode = auto, on active l'auto update
        window.withdraw()  # Cacher l'application pendant la mise à jour automatique
        update_button.config(state=tk.DISABLED, cursor=inactive_cursor)                                                          # On désactive le bouton Update
        Auto_Update(script_directory,websites,config,conn,cursor)
        window.deiconify()  # Réafficher l'application après la mise à jour automatique
    elif config['Update']['mode'].lower() == "manual":                                                              # Si mode = manual, on active l'update manuel
        update_button.config(command=lambda: Manual_Update(script_directory,selected_website,config,conn,cursor))
        button_hover(update_button, button_update_1, button_update_2)
    else:
        update_button.config(state=tk.DISABLED, cursor=inactive_cursor)                                                          # Action si le mode n'est pas reconnu
        driver.quit()                                                                                               # Fermer le navigateur
        print("\n Update Button inactive [set Update to 'manual' or 'auto' in settings] ")                                          ##### Track activity
    
    ######################################################################################################################################################################################

    # Action à exécuter lors de la fermeture de la fenêtre
    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    main()