import tkinter.filedialog as filedialog
import json
import os
import tkinter as tk
from tkinter import Toplevel, BooleanVar, Entry, Button, OptionMenu
from tkinter import Checkbutton, Canvas, PhotoImage, messagebox, StringVar
from .utils import button_hover, activate_button, deactivate_button
from foundation.core.essentials import relative_to_assets
from foundation.core.essentials import INACTIVE_CURSOR, ACTIVE_CURSOR
from foundation.core.essentials import PATH_TO_CONFIG, LOG


INFO_POLICE = ("Inter", 8 * -1)          # Police des INFOS
TITLE_POLICE = ("Inter Bold", 12 * -1)   # -||- des TITRES
CORPUS_POLICE = ("Inter Bold", 10 * -1)  # -||- alternative des TITRES
CURRENT_COLOR = "#FFFFFF"                # Couleur dominante du texte
ALT_COLOR = "#FFC700"                    # -||- alternative des INFOS
ENTRY_TEXT_COLOR = "#000716"             # -||- des entrées de texte
BACKGROUND_BUTTON_COLOR = "red"          # -||- d'arrière plan de bouton

settings_window = None                # État de la fenêtre
chromedriver_button_state = False       # État du bouton CHROMEDRIVER
update_button_state = True              # -||- UPDATE
download_button_state = True            # -||- DOWNLOAD
chromedriver_clicks = 0                 # nombre de clics sur (CHROMEDRIVER)
update_clicks = 0                       # -||- UPDATE
download_clicks = 0                     # -||- DOWNLOAD
save_clicks = 0                         # -||- SAVE

# CHROMEDRIVER_PAGE
TEXT_1 = "Path*"
TEXT_2 = "Path to your automated browser 🤖"
TEXT_3 = "Mode"
TEXT_4 = "Checked : automated browser can't be seen"
TEXT_5 = "Unchecked : automated browser can be seen"
# UPDATE_PAGE
TEXT_6 = "Mode"
TEXT_7 = "manual : manually update a website datas"
TEXT_8 = "auto : automatically update all websites datas when starting app"
TEXT_9 = "Websites"
TEXT_10 = "Enable [Checked] or Disable [Unchecked] any website’s update."
TEXT_11 = "Scantrad"
TEXT_12 = "Lelscans"
TEXT_13 = "Fmteam"
TEXT_14 = "Animesama"
# DOWNLOAD_PAGE
TEXT_15 = "Path"
TEXT_16 = "The folder where your scans'll be stored. ( Default : PandaScan 🐼 directory )"


def show_settings(main_window, SETTINGS, settings_button):
    """Afficher la fênetre Settings.

    Args:
        main_window (Any): master window
        SETTINGS (Any): fichier de configuration json
        settings_button (Any): bouton attaché à la fonction
    """

    global settings_window, update_mode_menu

    if settings_window is None:
        LOG.debug("Settings opened ⚙️")

        settings_window = Toplevel(main_window)
        settings_button.config(state="disabled")

        settings_window.geometry("483x319")
        settings_window.configure(bg=CURRENT_COLOR)
        settings_window.title("Settings ⚙️")

        canvas = Canvas(
            settings_window,
            bg=CURRENT_COLOR,
            height=319,
            width=483,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Stocker l'état des checkbox
        chromedriver_mode_var = BooleanVar(value=SETTINGS["driver"]["headless"])
        fmteam_checkbox_var = BooleanVar(value=SETTINGS["websites"]["fmteam"]["enabled"])
        lelscans_checkbox_var = BooleanVar(value=SETTINGS["websites"]["lelscans"]["enabled"])
        scantrad_checkbox_var = BooleanVar(value=SETTINGS["websites"]["scantrad"]["enabled"])
        animesama_checkbox_var = BooleanVar(value=SETTINGS["websites"]["animesama"]["enabled"])

        # Initialiser des dictionnaires [widgets + labels]
        widgets_to_manage = {}
        labels_to_manage = {}

        # === FUNCTIONS

        def on_closing():
            """Actions à effectuer à la fermeture de la fenêtre.
            """
            global save_clicks

            settings_button.config(state="normal")

            LOG.debug("Settings exited 🚪")
            os.system("clear")
            if save_clicks == 0:
                LOG.info("\nNo changes in Settings.")
            else:
                LOG.info("\nThere are some changes in Settings, please restart your app.")

            settings_window.withdraw()

        def choose_directory(entry):
            """Choisir un emplacement de dossier.

            Args:
                entry (Any): entrée d'insertion du chemin choisi
            """
            directory = filedialog.askdirectory()
            entry.delete(0, tk.END)     # Effacer le contenu de l'entrée
            entry.insert(0, directory)  # Insérer le chemin du dossier choisi

        def choose_file(entry):
            """Choisir un emplacement de fichier

            Args:
                entry (Any): entrée d'insertion du chemin choisi
            """
            file = filedialog.askopenfilename(title="select the chromedriver file")
            if file:
                entry.delete(0, tk.END)  # Effacer le contenu de l'entrée
                entry.insert(0, file)    # Insérer le chemin du fichier choisi

        def mask_elements(button):
            """Masquer un ou plusieurs widgets

            Args:
                button: bouton de référence
            """
            for element in widgets_to_manage[button].keys():
                element.place_forget()

        def hide_text(button):
            """Masquer un ou plusieurs elements textuels

            Args:
                button (Any): bouton de référence
            """
            for element in labels_to_manage[button].keys():
                canvas.itemconfig(element, state="hidden")

        def show_text(button):
            """Afficher un ou plusieurs elements textuels

            Args:
                button (Any): bouton de référence
            """
            for element in labels_to_manage[button].keys():
                canvas.itemconfig(element, state="normal")

        def show_elements(button):
            """Afficher les widgets cachés.

            Args:
                button (Any): bouton de référence
            """
            for element, (x, y, width, height) in widgets_to_manage[button].items():
                element.place(x=x, y=y, width=width, height=height)
            settings_window.update()

        def check_previous_deactivate_button(button):
            """Vérifier quel bouton était désactivé avant de désactiver le bouton actuel.

            Args:
                button (Any): bouton de référence
            """
            global chromedriver_clicks, chromedriver_button_state, update_clicks, update_button_state, download_clicks, download_button_state

            def manage_page_deactivation(button, button_image_1, button_image_2, window_state):
                """Masquer les éléments de la page correspondante

                Args:
                    button (Any): bouton de référence
                    button_image_1 (Any): image par défaut
                    button_image_2 (Any): image alternative
                    window_state (Any): état de la fenêtre

                Returns:
                    bool: état de la fenêtre
                """
                activate_button(button, button_image_1, button_image_2)
                hide_text(button)
                mask_elements(button)
                window_state = True

                return window_state

            # Chromedriver button
            if button == button_1:
                deactivate_button(button, chromedriver_page_2)
                chromedriver_clicks += 1
                if update_button_state is False:
                    update_button_state = manage_page_deactivation(button_2, update_page_1, update_page_2, update_button_state)
                elif download_button_state is False:
                    download_button_state = manage_page_deactivation(button_3, download_page_1, download_page_2, download_button_state)
            # Update button
            elif button == button_2:
                deactivate_button(button, update_page_2)
                update_clicks += 1
                if download_button_state is False:
                    download_button_state = manage_page_deactivation(button_3, download_page_1, download_page_2, download_button_state)
                elif chromedriver_button_state is False:
                    chromedriver_button_state = manage_page_deactivation(button_1, chromedriver_page_1, chromedriver_page_2, chromedriver_button_state)
            # Download button
            elif button == button_3:
                deactivate_button(button, download_page_2)
                download_clicks += 1
                if chromedriver_button_state is False:
                    chromedriver_button_state = manage_page_deactivation(button_1, chromedriver_page_1, chromedriver_page_2, chromedriver_button_state)
                elif update_button_state is False:
                    update_button_state = manage_page_deactivation(button_2, update_page_1, update_page_2, update_button_state)

        def manage_window(button):
            """Gérer l'affichage d'une page

            Args:
                button (Any): bouton de référence
            """
            check_previous_deactivate_button(button)
            show_elements(button)
            show_text(button)

        def chromedriver_settings():
            """Charger les éléments de la page Chromedriver
            """
            global chromedriver_button_state, chromedriver_clicks
            global chromedriver_entry, choose_file_path, chromedriver_checkbox
            global chromedriver_path, chromedriver_path_info, chromedriver_mode, chromedriver_checkbox_info_1, chromedriver_checkbox_info_2

            chromedriver_button_state = False

            if chromedriver_clicks != 0:
                manage_window(button_1)
                return

            # [ TEXT ]   Path*
            chromedriver_path = canvas.create_text(49.0, 75.0, anchor="nw", text=TEXT_1, fill=CURRENT_COLOR, font=TITLE_POLICE)
            # [ WIDGET ] Entry
            chromedriver_entry = Entry(settings_window, bd=0, bg=CURRENT_COLOR, fg=ENTRY_TEXT_COLOR, highlightthickness=0)
            chromedriver_entry.insert(0, SETTINGS["chromedriver_path"])
            chromedriver_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
            # [ WIDGET ] Button choose file
            choose_file_path = Button(settings_window, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, text="Search", font=CORPUS_POLICE, command=lambda: choose_file(chromedriver_entry))
            choose_file_path.configure(highlightbackground=BACKGROUND_BUTTON_COLOR)
            choose_file_path.place(x=340.0, y=70.0, width=50.0, height=25.0)
            # [ TEXT ]   Info path
            chromedriver_path_info = canvas.create_text(93.0, 95.0, anchor="nw", text=TEXT_2, fill=CURRENT_COLOR, font=INFO_POLICE)
            # [ TEXT ]   Mode chromedriver
            chromedriver_mode = canvas.create_text(49.0, 110.0, anchor="nw", text=TEXT_3, fill=CURRENT_COLOR, font=TITLE_POLICE)
            # [ WIDGET ] Checkbox
            chromedriver_checkbox = Checkbutton(settings_window, variable=chromedriver_mode_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            chromedriver_checkbox.place(x=93.0, y=113.0, width=14.0, height=12.0)
            # [ TEXT ]   Infos checkbox
            chromedriver_checkbox_info_1 = canvas.create_text(93.0, 130.0, anchor="nw", text=TEXT_4, fill=CURRENT_COLOR, font=INFO_POLICE)
            chromedriver_checkbox_info_2 = canvas.create_text(93.0, 142.0, anchor="nw", text=TEXT_5, fill=ALT_COLOR, font=INFO_POLICE)

            # Les widgets à gérer
            widgets_to_manage[button_1] = {
                chromedriver_entry: (92.0, 76.0, 228.0, 13.0),
                choose_file_path: (340.0, 70.0, 50.0, 25.0),
                chromedriver_checkbox: (93.0, 113.0, 14.0, 12.0)
            }
            # Les labels à gérer
            labels_to_manage[button_1] = {
                chromedriver_path: (49.0, 75.0),
                chromedriver_path_info: (93.0, 95.0),
                chromedriver_mode: (49.0, 110.0),
                chromedriver_checkbox_info_1: (93.0, 130.0),
                chromedriver_checkbox_info_2: (93.0, 142.0)
            }

            chromedriver_clicks = 1

        def update_settings():
            """Charger les éléments de la page update
            """
            global update_button_state, update_clicks
            global update_mode_menu, update_checkbox_1, update_checkbox_2, update_checkbox_3
            global update_mode, update_mode_info_1, update_mode_info_2, update_websites, update_websites_info, update_scantrad, update_lelscan, update_fmteam
            global update_mode_var

            update_button_state = False

            if update_clicks != 0:
                manage_window(button_2)
                return

            # [ TEXT ]   Update mode
            update_mode = canvas.create_text(49.0, 75.0, anchor="nw", text=TEXT_6, fill=CURRENT_COLOR, font=TITLE_POLICE)
            # [ WIDGET ] Menu [Update mode]
            update_mode_var = StringVar(settings_window)
            update_mode_var.set(SETTINGS["Update"]["mode"])
            update_mode_menu = OptionMenu(settings_window, update_mode_var, "manual", "auto")
            update_mode_menu.place(x=92.0, y=76.0)
            update_mode_menu.configure(bg=CURRENT_COLOR)
            # [ TEXT ]   Infos [Update mode]
            update_mode_info_1 = canvas.create_text(93.0, 96.0, anchor="nw", text=TEXT_7, fill=CURRENT_COLOR, font=INFO_POLICE)
            update_mode_info_2 = canvas.create_text(93.0, 108.0, anchor="nw", text=TEXT_8, fill=ALT_COLOR, font=INFO_POLICE)
            # [ TEXT ]   Websites
            update_websites = canvas.create_text(49.0, 125.0, anchor="nw", text=TEXT_9, fill=CURRENT_COLOR, font=TITLE_POLICE)
            # [ TEXT ]   Info [Websites]
            update_websites_info = canvas.create_text(50.0, 140.0, anchor="nw", text=TEXT_10, fill=CURRENT_COLOR, font=INFO_POLICE)
            # [ TEXT ]   Scantrad
            update_scantrad = canvas.create_text(65.0, 158.0, anchor="nw", text=TEXT_11, fill=CURRENT_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_1 [Scantrad]
            update_checkbox_1 = Checkbutton(settings_window, variable=scantrad_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_1.place(x=125.0, y=158.0, width=14.0, height=12.0)
            # [ TEXT ]   Lelscans
            update_lelscan = canvas.create_text(65.0, 176.0, anchor="nw", text=TEXT_12, fill=CURRENT_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_2 [Lelscan]
            update_checkbox_2 = Checkbutton(settings_window, variable=lelscans_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_2.place(x=125.0, y=176.0, width=14.0, height=12.0)
            # [ TEXT ]   Fmteam
            update_fmteam = canvas.create_text(65.0, 196.0, anchor="nw", text=TEXT_13, fill=CURRENT_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_3 [Fmteam]
            update_checkbox_3 = Checkbutton(settings_window, variable=fmteam_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_3.place(x=125.0, y=196.0, width=14.0, height=12.0)
            # [ TEXT ]   Animesama
            update_animesama = canvas.create_text(65.0, 216.0, anchor="nw", text=TEXT_14, fill=CURRENT_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_4 [Animesama]
            update_checkbox_4 = Checkbutton(settings_window, variable=animesama_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_4.place(x=125.0, y=216.0, width=14.0, height=12.0)

            # Les widgets à gérer
            widgets_to_manage[button_2] = {
                update_mode_menu: (92.0, 76.0, 80, 15.0),
                update_checkbox_1: (125.0, 158.0, 14.0, 12.0),
                update_checkbox_2: (125.0, 176.0, 14.0, 12.0),
                update_checkbox_3: (125.0, 196.0, 14.0, 12.0),
                update_checkbox_4: (125.0, 216.0, 14.0, 12.0)}
            # Les labels à gérer
            labels_to_manage[button_2] = {
                update_mode: (49.0, 75.0),
                update_mode_info_1: (93.0, 96.0),
                update_mode_info_2: (93.0, 108.0),
                update_websites: (49.0, 125.0),
                update_websites_info: (50.0, 140.0),
                update_scantrad: (65.0, 158.0),
                update_lelscan: (65.0, 176.0),
                update_fmteam: (65.0, 196.0),
                update_animesama: (65.0, 216.0)}

            check_previous_deactivate_button(button_2)

        def download_settings():
            """Charger les éléments de la page DOWNLOAD
            """
            global download_button_state, download_clicks
            global download_entry, choose_directory_path
            global download_path, download_path_info

            download_button_state = False

            if download_clicks != 0:
                manage_window(button_3)
                return

            # [ TEXT ]   Path
            download_path = canvas.create_text(55.0, 75.0, anchor="nw", text=TEXT_15, fill=CURRENT_COLOR, font=TITLE_POLICE)
            # [ WIDGET ] Entry
            download_entry = Entry(settings_window, bd=0, bg=CURRENT_COLOR, fg=ENTRY_TEXT_COLOR, highlightthickness=0)
            download_entry.insert(0, SETTINGS["Download"]["path"])
            download_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
            # [ WIDGET ] Choose directory button
            choose_directory_path = Button(settings_window, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, text="Search", font=CORPUS_POLICE, command=lambda: choose_directory(download_entry))
            choose_directory_path.configure(highlightbackground=BACKGROUND_BUTTON_COLOR)
            choose_directory_path.place(x=340.0, y=70.0, width=50.0, height=25.0)
            # [ TEXT ]   Info path
            download_path_info = canvas.create_text(55.0, 100.0, anchor="nw", text=TEXT_16, fill=CURRENT_COLOR, font=INFO_POLICE)

            # Les widgets à gérer
            widgets_to_manage[button_3] = {
                download_entry: (92.0, 76.0, 228.0, 13.0),
                choose_directory_path: (340.0, 70.0, 50.0, 25.0)}
            # Les labels à gérer
            labels_to_manage[button_3] = {
                download_path: (55.0, 75.0),
                download_path_info: (55.0, 100.0)}

            check_previous_deactivate_button(button_3)

        def save_settings():
            """Sauvegarder les changements dans le fichier de configuration.
            """
            global save_clicks

            save_confirm = messagebox.askquestion(message=" Save new settings ❓")

            if save_confirm == "yes":
                SETTINGS["chromedriver_path"] = chromedriver_entry.get()
                SETTINGS["driver"]["headless"] = chromedriver_mode_var.get()
                SETTINGS["Update"]["mode"] = update_mode_var.get()
                SETTINGS["websites"]["fmteam"]["enabled"] = fmteam_checkbox_var.get()
                SETTINGS["websites"]["lelscans"]["enabled"] = lelscans_checkbox_var.get()
                SETTINGS["websites"]["scantrad"]["enabled"] = scantrad_checkbox_var.get()
                SETTINGS["websites"]["animesama"]["enabled"] = animesama_checkbox_var.get()
                SETTINGS["Download"]["path"] = download_entry.get()

                with open(PATH_TO_CONFIG, 'w') as json_file:
                    json.dump(SETTINGS, json_file, indent=4)

                save_clicks += 1

                return LOG.debug("New settings saved ✅")

            else:

                save_clicks = 0
                return LOG.debug("Saving canceled ❌")

        # === FOUNDATION

        # Background
        background = PhotoImage(file=relative_to_assets("background.png"))
        canvas.create_image(241.0, 159.0, image=background)

        # App logo
        app_logo_m = PhotoImage(file=relative_to_assets("app_logo_m.png"))
        canvas.create_image(449.0, 23.0, image=app_logo_m)

        # Foreground
        foreground = PhotoImage(file=relative_to_assets("foreground.png"))
        canvas.create_image(241.0, 179.0, image=foreground)

        # === BUTTONS

        # CHROMEDRIVER
        chromedriver_page_2 = PhotoImage(file=relative_to_assets("chromedriver_page_2.png"))
        chromedriver_page_1 = PhotoImage(file=relative_to_assets("chromedriver_page_1.png"))
        button_1 = Button(
            settings_window,
            image=chromedriver_page_2,
            borderwidth=0,
            highlightthickness=0,
            command=chromedriver_settings,
            relief="flat",
            state=tk.DISABLED,
            cursor=INACTIVE_CURSOR
        )
        button_1.place(x=29, y=23, width=108, height=28)

        # UPDATE
        update_page_2 = PhotoImage(file=relative_to_assets("update_page_2.png"))
        update_page_1 = PhotoImage(file=relative_to_assets("update_page_1.png"))
        button_2 = Button(
            settings_window,
            image=update_page_1,
            borderwidth=0,
            highlightthickness=0,
            command=update_settings,
            relief="flat",
            state=tk.NORMAL,
            cursor=ACTIVE_CURSOR
        )
        button_2.place(x=157, y=24, width=61, height=27)
        button_hover(button_2, update_page_1, update_page_2)

        # DOWNLOAD
        download_page_2 = PhotoImage(file=relative_to_assets("download_page_2.png"))
        download_page_1 = PhotoImage(file=relative_to_assets("download_page_1.png"))
        button_3 = Button(
            settings_window,
            image=download_page_1,
            borderwidth=0,
            highlightthickness=0,
            command=download_settings,
            relief="flat",
            state=tk.NORMAL,
            cursor=ACTIVE_CURSOR
        )
        button_3.place(x=237, y=23, width=80, height=28)
        button_hover(button_3, download_page_1, download_page_2)

        # SAVE
        save_button_2 = PhotoImage(file=relative_to_assets("save_button_2.png"))
        save_button_1 = PhotoImage(file=relative_to_assets("save_button_1.png"))
        button_4 = Button(
            settings_window,
            image=save_button_1,
            borderwidth=0,
            highlightthickness=0,
            command=save_settings,
            relief="flat",
            state=tk.NORMAL,
            cursor=ACTIVE_CURSOR
        )
        button_4.place(x=210, y=271, width=91, height=25)
        button_hover(button_4, save_button_1, save_button_2)

        # Load elements
        chromedriver_settings()
        update_settings()
        download_settings()
        # Set CHROMEDRIVER as the default page to display
        chromedriver_settings()
        settings_window.protocol("WM_DELETE_WINDOW", on_closing)
        settings_window.resizable(False, False)
        settings_window.mainloop()

    else:
        settings_window.deiconify()
