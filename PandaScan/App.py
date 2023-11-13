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
# This project aims to download mangas scans with ease for a local access and private use.
# For now, Chromedriver is required to use PandaScan. Please follow the 'README' file.
# You are now able to change Settings directly in App.
#    ° Choose between "manual" or "auto" update.
#    ° Select where to save your scans after a download.
#    ° Updating PandaScan generates changelogs files | Ckeck changelogs in 'changelog > choose a website > changelog.txt'
# Please note that some websites may provide empty docs when downloading (especially scantrad)
# If you like this project, please consider giving it a ⭐️ on Github.🫶
# Credits: @Tkinter-designer by ParthJadhav
# ------------------------------------------------------------------------------------------------------------


import os
import tkinter as tk
from tkinter import Tk, ttk, Canvas, Entry, Listbox
from tkinter import Scrollbar, Button, Checkbutton, Label
from tkinter import PhotoImage, StringVar, OptionMenu, messagebox
from download.manage import download
from update.manage import manual_update, auto_update
from gui.Settings import show_settings
from gui.utils import button_hover
from foundation.core.essentials import relative_to_assets, check_connection
from foundation.core.essentials import INACTIVE_CURSOR, ACTIVE_CURSOR, CONN, SELECTOR
from foundation.core.essentials import WEBSITES, MAIN_DIRECTORY, DRIVER, SETTINGS, LOG


POLICE_1 = ("Inter", 15 * -1)
POLICE_2 = ("Inter", 16 * -1)
CURRENT_COLOR = "#FFFFFF"                     # dominant text color
ALT_COLOR = "#6B0000"                         # -||- info text color
ENTRY_TEXT_COLOR = "#000716"                  # -||- entry text color

default_website = WEBSITES[0]                 # website selected
nb_of_manga_chapters = 0                      # number of chapters from a manga (total)
nb_of_chapters_to_download = 0                # number of chapters to download
download_id = 0                               # id of the current download
selected_manga_name = ''                      # name of the selected manga
selected_manga_chapters = []                  # list that contains the selected chapters
download_button_state = False                 # state of the download button
manga_file_path = ''                          # path to the manga folder

TEXT_1 = "🌐"
TEXT_2 = "Manga name"
TEXT_3 = "Chapter / Volume"
TEXT_4 = "Select All"


def main():
    """Charger les éléments de l'application
    """

    if not check_connection():
        messagebox.showinfo("Error [🛜]", "😵‍💫 Oups, no internet connection detected ❗️")
        return print("\nPandascan exited 🚪\n")

    print("Pandascan launched ✅\n")

    main_window = Tk()

    main_window.title("PandaScan 🐼")

    main_window.geometry("962x686")
    main_window.configure(bg=CURRENT_COLOR)
    canvas = Canvas(
        main_window,
        bg=CURRENT_COLOR,
        height=686,
        width=962,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # === FUNCTIONS

    def on_closing():
        """Actions à effectuer à la fermeture de l'application.
        """
        if DRIVER:
            DRIVER.quit()
        CONN.close()
        main_window.destroy()
        print("\nApp closed 👋.\n")

    def Reload_page():
        """Reinitialise les widgets de l'application.
        """
        global selected_manga_name

        selected_manga_name = ''

        entry_1.delete(0, tk.END)
        canvas.itemconfigure(Chapter_selected, text='')
        canvas.itemconfigure(Manga_selected, text='')
        result_box.delete(0, tk.END)
        chapters_box.delete(0, tk.END)

    def Switch_Website(*args):
        """Changer de site de scrapping.
        """
        global default_website

        selected_item = website_list_var.get()
        default_website = selected_item
        LOG.debug(f"Website : {selected_item}")
        Reload_page()

    def select_all():
        """Sélectionner tous les chapitres d'un manga en cliquant sur la CheckBox.
        """
        global nb_of_manga_chapters, selected_manga_name, selected_manga_chapters

        if select_all_var.get() == 1:
            chapters_box.select_set(0, tk.END)  # sélectionner tous les éléments de la ChapterBox
            query = "SELECT Chapitres FROM Chapitres WHERE NomSite = ? AND NomManga = ?"
            SELECTOR.execute(query, (default_website, selected_manga_name))
            results = SELECTOR.fetchall()
            selected_manga_chapters = [chapitre[0] for chapitre in results]  # créer une liste composée des chapitres sélectionnés

            LOG.debug(selected_manga_chapters)
            nb_of_manga_chapters = len(selected_manga_chapters)
            canvas.itemconfigure(Chapter_selected, text=f'{nb_of_manga_chapters} selected')
        else:
            chapters_box.selection_clear(0, tk.END)  # désélectionner tous les éléments de la ListBox
            selected_manga_chapters = []  # réinitialiser la sélection des chapitres
            LOG.debug(selected_manga_chapters)
            canvas.itemconfigure(Chapter_selected, text='0 selected')

    def update_results(event):
        """Update les résultats dans la liste des mangas

        Args:
            event (Any): L'événement qui déclenche la fonction
        """
        global default_website

        keyword = entry_1.get()  # Récupérer l'entrée de la searchbar
        keyword = '%' + keyword + '%'
        query = "SELECT NomManga FROM Mangas WHERE NomManga LIKE ? AND NomSite = ?"
        SELECTOR.execute(query, (keyword, default_website))  # Chercher les correspondances dans la DB
        results = [row[0] for row in SELECTOR.fetchall()]  # Récupérer les correspondances
        result_box.delete(0, tk.END)   # Supprimer les anciens résultats s'il y'en avaient
        result_box.insert(tk.END, *results)  # Insérer les nouveaux résultats dans la Manga_list box

    def on_mangas_select(event):
        """Actions lorsqu'un manga est sélectionné

        Args:
            event (Any): L'événement qui déclenche la fonction
        """
        global selected_manga_name

        selected_indices = result_box.curselection()  # récupérer l'indice de l'élément sélectionné
        if selected_indices:
            manga_name = result_box.get(selected_indices[0])    # récupérer le nom du manga
            selected_manga_name = manga_name
            update_chapters(manga_name)
            truncated_text = manga_name[:15] + "..." if len(manga_name) > 15 else manga_name
            canvas.itemconfigure(Manga_selected, text=truncated_text)

    def update_chapters(manga_name):
        """Update les résultats dans la Chapter List lorsqu'un manga est sélectionné

        Args:
            manga_name (str): Le nom du manga sélectionné
        """
        global default_website

        # Rechercher tous les chapitres du manga sélectionné
        query = "SELECT Chapitres FROM Chapitres WHERE NomSite = ? AND NomManga = ?"
        SELECTOR.execute(query, (default_website, manga_name))
        results = [result[0] for result in SELECTOR.fetchall()]  # Utilisation d'indices
        chapters_box.delete(0, tk.END)  # Effacer le contenu précédent de la liste déroulante

        # Afficher les résultats dans la ChapterBox
        chapters_box.insert(tk.END, *results)  # Utilisation de l'opérateur * pour insérer tous les chapitres

        if select_all_var.get() == 1:
            select_all()

    def on_chapters_select(event):
        """Actions lorsque des chapitres sont sélectionnés

        Args:
            event (Any): L'événement qui déclenche la fonction
        """
        global selected_manga_chapters, nb_of_manga_chapters

        selected_chapters = chapters_box.curselection()  # récupérer les indices des chapitres sélectionnés
        selected_manga_chapters = [chapters_box.get(index) for index in selected_chapters]  # récupérer les chapitres sélectionnés
        nb_of_manga_chapters = len(selected_manga_chapters)
        canvas.itemconfigure(Chapter_selected, text=f'{nb_of_manga_chapters} selected')

    def Set_download():
        """Gérer les téléchargements des chapitres sélectionnés
        """
        global download_id

        # Réinitialiser l'id de téléchargement
        download_id = 0

        def Hide_DownloadBox():
            """Cacher la barre d'infos des téléchargement
            """
            canvas.itemconfigure(image_1, state=tk.HIDDEN)

        def Start_download():
            """Lancer le téléchargement d'un chapitre
            """
            global download_id, download_button_state

            chapter_name = selected_manga_chapters[download_id]
            if os.path.exists(SETTINGS['Download']['path']):
                chapter_name_path = manga_file_path + '/' + chapter_name
            else:
                chapter_name_path = manga_file_path / chapter_name

            download(default_website, chapter_name_path, selected_manga_name, download_id, chapter_name, manga_file_path, SETTINGS, SELECTOR)

            download_id += 1
            if nb_of_manga_chapters > 1:
                progress = int((download_id / nb_of_manga_chapters) * 100)
                progressbar["value"] = progress
                percentage_label["text"] = f"{progress}%"
                main_window.update_idletasks()

            if download_id < nb_of_manga_chapters:
                main_window.after(1000, Start_download)
            else:
                if nb_of_manga_chapters > 1:
                    progressbar.place_forget()
                    percentage_label.place_forget()
                messagebox.showinfo("Info [ℹ️]", "Successfull Download ✅\n Thanks for using PandaScan 🐼")
                Hide_DownloadBox()
                download_button.configure(state="normal")  # Réactiver le bouton de téléchargement
                download_button_state = False
                LOG.info(f"Download completed ✅\n\nStored at : {manga_file_path}")

        def Manage_DownloadBox():
            """Désactiver le bouton de téléchargement et gérer la barre d'infos des téléchargements
            """
            global download_button_state

            download_button_state = True
            download_button.configure(state="disabled")
            if nb_of_manga_chapters > 1:  # afficher la barre de progression si plus d'un chapitre est sélectionné
                canvas.itemconfigure(image_1, state=tk.NORMAL)
                progressbar.place(x=800.0, y=520.0)
                percentage_label.place(x=830.0, y=545.0)

            Start_download()

        def Set_download_directory():
            """Gérer le chemin de destination des téléchargements
            """
            global manga_file_path

            if os.path.exists(SETTINGS['Download']['path']):
                manga_file_path = SETTINGS['Download']['path'] + '/' + selected_manga_name
            else:
                manga_file_path = MAIN_DIRECTORY / selected_manga_name
                if not os.path.exists(manga_file_path):
                    os.makedirs(manga_file_path)

            Manage_DownloadBox()

        if nb_of_manga_chapters == 0:
            messagebox.showinfo("Info [ℹ️]", "No Chapter Selected 🤕, Try again")
        else:
            os.system("clear")
            LOG.info(f"Downloading {selected_manga_name} ..")
            Set_download_directory()

    # === BASIC ELEMENTS

    # App Name
    Name_App = PhotoImage(file=relative_to_assets("Name_App.png"))
    canvas.create_image(481.0, 65.0, image=Name_App)
    # App Logo
    Logo_App = PhotoImage(file=relative_to_assets("Logo_App.png"))
    canvas.create_image(85.0, 65.0, image=Logo_App)
    # Searchbar Background
    SearchBar_background = PhotoImage(file=relative_to_assets("SearchBar_background.png"))
    canvas.create_image(495.0, 209.0, image=SearchBar_background)
    # Searchbar Foreground
    SearchBar_foreground = PhotoImage(file=relative_to_assets("SearchBar_foreground.png"))
    canvas.create_image(511.0, 202.0, image=SearchBar_foreground)

    # === Barre de recherche de mangas ( SearchBar )

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(510.5, 204.0, image=entry_image_1)
    entry_1 = Entry(main_window, bd=0, bg=CURRENT_COLOR, fg=ENTRY_TEXT_COLOR, highlightthickness=0)
    entry_1.place(x=376.0, y=195.0, width=269.0, height=16.0)

    # === Choix déroulant du site web

    canvas.create_text(413.0, 152.0, anchor="nw", text=TEXT_1, fill=CURRENT_COLOR, font=POLICE_1)
    website_list_var = StringVar(main_window)
    website_list_var.set(default_website)  # Default website
    website_menu = OptionMenu(
        main_window,
        website_list_var,
        WEBSITES[0],
        WEBSITES[1],
        WEBSITES[2]
    )
    website_menu.place(x=440.0, y=150.0)
    website_menu.configure(bg=CURRENT_COLOR)

    # Associer la fonction au changement de site
    website_list_var.trace_add("write", Switch_Website)

    # === Zone d'affichage des Chapitres ( ChapterBox : Image )

    Chapters_list_Box = PhotoImage(file=relative_to_assets("Chapters_list_Box.png"))
    canvas.create_image(588.0, 392.0, image=Chapters_list_Box)

    # === Zone d'affichage des noms de Mangas ( MangaBox : Image )

    Manga_name_listBox = PhotoImage(file=relative_to_assets("Manga_name_listBox.png"))
    canvas.create_image(382.0, 392.0, image=Manga_name_listBox)

    # === Zone d'affichage des noms de Mangas ( MangaBox )

    canvas.create_text(331.0, 269.0, anchor="nw", text=TEXT_2, fill=CURRENT_COLOR, font=POLICE_1)

    # Liste d'affichage des noms de mangas
    result_box = Listbox(main_window, selectmode=tk.SINGLE)
    result_box.place(x=306, y=300, width=150, height=190)
    # Scrollbar associée à la liste des noms de mangas
    result_scrollbar = Scrollbar(main_window)
    result_scrollbar.place(x=265, y=300, height=190)

    # Lié la scrollbar à la liste de noms de mangas et vice versa
    result_scrollbar.config(command=result_box.yview)
    result_box.config(yscrollcommand=result_scrollbar.set, bd=0)

    # === Zone d'affichage des Chapitres ( ChapterBox )

    canvas.create_text(525.0, 269.0, anchor="nw", text=TEXT_3, fill=CURRENT_COLOR, font=POLICE_1)

    # Liste d'affichage des chapitres
    chapters_box = Listbox(main_window, selectmode=tk.MULTIPLE)
    chapters_box.place(x=535.0, y=300.0, width=100, height=190)
    # Scrollbar associée à la liste des chapitres
    chapters_scrollbar = Scrollbar(main_window)

    # Lié la scrollbar à la liste de chapitres et vice versa
    chapters_scrollbar.config(command=chapters_box.yview)
    chapters_scrollbar.place(x=685, y=300, height=190)                       # Barre de défilement
    chapters_box.config(yscrollcommand=chapters_scrollbar.set, bd=0)         # Liste

    # ===  Association des évènements

    # Recherche du manga + mise à jour des résultats
    entry_1.bind('<KeyRelease>', update_results)
    # Sélection du manga + affichage dans la box correspondante
    result_box.bind('<<ListboxSelect>>', on_mangas_select)
    # Sélection des chapitres + affichage du nombre de chapitres sélectionnés
    chapters_box.bind('<<ListboxSelect>>', on_chapters_select)

    # === Informations au cours d'un téléchargement

    Info_download = PhotoImage(file=relative_to_assets("Info_download.png"))
    image_1 = canvas.create_image(843.0, 575.0, image=Info_download, state=tk.HIDDEN)  # Cacher l'image au lancement de l'application
    # Barre de progression
    progressbar = ttk.Progressbar(main_window, mode="determinate")
    # Pourcentage de progression
    percentage_label = Label(main_window, text="0%", bg="white")

    # === Select all ( Checkbox )

    select_all_var = tk.IntVar()
    Check_box = Checkbutton(main_window, text=TEXT_4, variable=select_all_var, command=select_all, bg="white")
    Check_box.place(x=547.0, y=525.0)

    # === nombre de chapitres sélectionnés ( Chapters_info Box )

    chapters_info_box = PhotoImage(file=relative_to_assets("Chapters_info.png"))
    canvas.create_image(588.0, 584.0, image=chapters_info_box)
    # Nombre de Chapitres sélectionnés
    Chapter_selected = canvas.create_text(550.0, 570.0, anchor="nw", text="", fill=ALT_COLOR, font=POLICE_2)

    # === nom du manga sélectionné ( Manga_info Box )

    Manga_name_info_box = PhotoImage(file=relative_to_assets("Manga_name_info.png"))
    canvas.create_image(381.0, 584.0, image=Manga_name_info_box)
    # Manga Sélectionné
    Manga_selected = canvas.create_text(305.0, 570.0, anchor="nw", text="", fill=ALT_COLOR, font=POLICE_2)

    # === BUTTONS

    # DOWNLOAD
    button_download_2 = PhotoImage(file=relative_to_assets("Download_2.png"))
    button_download_1 = PhotoImage(file=relative_to_assets("Download_1.png"))
    download_button = Button(
        main_window,
        image=button_download_1,
        borderwidth=0,
        highlightthickness=0,
        command=Set_download,
        relief="flat",
        cursor=ACTIVE_CURSOR
    )
    download_button.place(x=801.0, y=584.0, width=95.0, height=93)
    button_hover(download_button, button_download_1, button_download_2, download_button_state)

    # SETTINGS
    button_settings_2 = PhotoImage(file=relative_to_assets("Settings_2.png"))
    button_settings_1 = PhotoImage(file=relative_to_assets("Settings_1.png"))
    settings_button = Button(
        main_window,
        image=button_settings_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_settings(main_window, SETTINGS, settings_button),
        relief="flat",
        cursor=ACTIVE_CURSOR
    )
    settings_button.place(x=830.0, y=25.0, width=108.0, height=40)
    button_hover(settings_button, button_settings_1, button_settings_2, download_button_state)

    # UPDATE
    button_update_2 = PhotoImage(file=relative_to_assets("Update_2.png"))
    button_update_1 = PhotoImage(file=relative_to_assets("Update_1.png"))
    update_button = Button(
        main_window,
        image=button_update_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        cursor=ACTIVE_CURSOR
    )
    update_button.place(x=664.0, y=57.0, width=41.0, height=44.0)

    if SETTINGS['Update']['mode'] == "auto":
        # Activer l'update automatique
        # Cacher l'application pendant la mise à jour automatique
        # Désactiver le bouton Update
        # Réafficher l'application après la mise à jour automatique
        main_window.withdraw()
        update_button.config(state=tk.DISABLED, cursor=INACTIVE_CURSOR)
        auto_update(MAIN_DIRECTORY, WEBSITES, SETTINGS, CONN, SELECTOR, LOG)
        main_window.deiconify()
    elif SETTINGS['Update']['mode'] == "manual":
        # Activer l'update manuelle
        update_button.config(command=lambda: manual_update(MAIN_DIRECTORY, default_website, SETTINGS, CONN, SELECTOR, WEBSITES, LOG))
        button_hover(update_button, button_update_1, button_update_2, download_button_state)

    main_window.protocol("WM_DELETE_WINDOW", on_closing)
    main_window.resizable(False, False)
    main_window.mainloop()


if __name__ == "__main__":
    main()
