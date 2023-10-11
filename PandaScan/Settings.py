from pathlib import Path
import tkinter.filedialog as filedialog
import json
import tkinter as tk
from tkinter import Canvas, PhotoImage, messagebox
from Update import script_directory

# To-do-list :
# Nettoyer le code

################################    Variables Globales   ############################################
settings_window = None
Chromedriver_window = False                     # Désactivé par défaut ( on ne peut plus cliquer dessus )
Update_window = True                            # Activé par défaut ( on peut cliquer dessus )
Download_window = True                          # Activé par défaut ( on peut cliquer dessus )
info_police = ("Inter", 8 * -1)                 # Police des infos
title_police = ("Inter Bold", 12 * -1)          # Police des titres
corpus_police = ("Inter Bold", 10 * -1)         # Autre Police du texte
current_color = "#FFFFFF"                       # Couleur du texte normal ( blanc )
alt_color = "#8C4040"                           # Couleur alternative pour le texte [Info] ( rouge )
entry_textcolor = "#000716"                     # Couleur du texte dans les barres d'entrées 
background_button_color = "red"                 # couleur d'arrière plan des boutons 'Search'
inactive_cursor = "arrow"                       # Curseur par défaut
active_cursor = "hand2"                         # Curseur lorsque la souris survole un bouton                                        
Chromedriver_clicked = 0                        # Variable pour savoir si onn a déjà cliquer sur le bouton chromedriver
Update_clicked = 0                              # Variable pour savoir si onn a déjà cliquer sur le bouton Update
Download_clicked = 0                            # Variable pour savoir si onn a déjà cliquer sur le bouton Download
save_clicked = 0                                # Variable pour savoir si onn a déjà cliquer sur le bouton Save
#######################################################################################################

# chemin relatif vers les assets de l'application
assets_directory = script_directory / "assets"

########################################################    MAIN FUNCTION    ############################################################
def show_settings(window, config, settings_button):
    """Afficher la fênetre Settings.
    """
    global settings_window, update_entry

    if settings_window is None:

        print("\nSettings opened ⚙️")
        settings_window = tk.Toplevel(window)
        settings_button.config(state="disabled")  # Désactiver le bouton settings

        settings_window.geometry("483x319")
        settings_window.configure(bg = current_color)
        settings_window.title("Settings ⚙️")

        canvas = Canvas(
            settings_window,
            bg = current_color,
            height = 319,
            width = 483,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        
        # Stocker l'état des checkbox
        chromedriver_mode_var = tk.BooleanVar(value=config["driver"]["headless"]) 
        fmteam_checkbox_var = tk.BooleanVar(value=config["websites"]["fmteam.fr"]["enabled"])
        lelscans_checkbox_var = tk.BooleanVar(value=config["websites"]["lelscans.net"]["enabled"])
        scantrad_checkbox_var = tk.BooleanVar(value=config["websites"]["scantrad-vf"]["enabled"])

        # =============================================================================    FUNCTIONS    ==================================================================================================
        def relative_to_assets(path: str) -> Path:
            """Get the relative path to the assets folder."""        
            return assets_directory / Path(path)
    
        def on_closing(): 
            """Actions à effectuer à la fermeture de l'application
            """
            global save_clicked
            
            settings_button.config(state="normal")  # Réactiver le bouton settings

            print("\nSettings exited 🚪\n")         # Afficher le message de sortie des paramètres
            if save_clicked == 0:
                print("[INFO ℹ️ ] No changes in Settings.\n")
            else:
                print("[INFO ℹ️ ] There are Changes in Settings.\n")
            
            settings_window.withdraw()

        def choose_directory(entry):
            """Choisir un emplacement de dossier

            Args:
                entry (Any): entrée dans laquelle le chemin du dossier choisi sera inséré
            """        
            directory = filedialog.askdirectory()
            entry.delete(0, tk.END)  # Effacer le contenu actuel de l'entrée
            entry.insert(0, directory)  # Insérer le chemin du dossier choisi dans l'entrée

        def choose_file(entry):
            """Choisir un emplacement de fichier

            Args:
                entry (Any): entrée dans laquelle le chemin du fichier choisi sera inséré
            """        
            file = filedialog.askopenfilename(title="select the chromedriver file")
            if file:
                entry.delete(0, tk.END) # Effacer le contenu actuel de l'entrée
                entry.insert(0, file)   # Insérer le chemin du fichier choisi dans l'entrée
                
        def mask_elements(*elements):
            """Masquer un ou plusieurs widegts

            Args:
                *elements: Tuple contenant les éléments à masquer
            """
            for element in elements:
                element.place_forget()  

        def hide_text(*elements):
            """Masquer un ou plusieurs elements textuels
            """        
            for element in elements:
                canvas.itemconfig(element, state="hidden")

        def show_text(*elements):
            """Afficher un ou plusieurs elements textuels
            """        
            for element in elements:
                canvas.itemconfig(element, state="normal")
        
        def show_elements(button):
            """Replacer les widgets cachés correspondant au bouton.

            Args:
                button (Any): le bouton / la page concernée.
            """

            if button == button_1:                                                                  # Chromedriver
                chromedriver_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
                choose_file_path.place(x=340.0, y=70.0, width=50.0, height=25.0)
                chromedriver_checkbox.place(x=93.0, y=113.0, width=14.0, height=12.0)
            elif button == button_2:                                                                # Update
                update_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
                update_checkbox_1.place(x=118.0, y=158.0, width=14.0, height=12.0)
                update_checkbox_2.place(x=118.0, y=176.0, width=14.0, height=12.0)
                update_checkbox_3.place(x=118.0, y=196.0, width=14.0, height=12.0)
            elif button == button_3:                                                                # Download
                download_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
                choose_directory_path.place(x=340.0, y=70.0, width=50.0, height=25.0)                                                             
                
        def button_hover(button,button_image_1,button_image_2):
            """Activer le Hover du bouton

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
                    button.configure(image=button_image)

            button.bind("<Enter>", lambda event:set_button_color(event, button, button_image_2))
            button.bind("<Leave>", lambda event:set_button_color(event, button, button_image_1))

        def deactivate_hover(button):
            """ Désactiver le Hover du bouton.

            Args:
                button (_type_): le bouton qui déclenche la fonction
            """
            button.unbind("<Enter>")
            button.unbind("<Leave>")
            
        def activate_button(button,button_image_1,button_image_2):
            """Activer un bouton

            Args:
                button_image_1 (Any): l'image par défaut du bouton
                button_image_2 (Any): l'image lorsque la souris survole le bouton
            """        
            button.config(image=button_image_1, state=tk.NORMAL, cursor=active_cursor)
            button_hover(button,button_image_1,button_image_2)

        def deactivate_button(button,button_image_2):
            """Désactiver un bouton

            Args:
                button (Any): le bouton à désactiver
                button_image_2 (Any): l'image lorsque la souris survole le bouton
            """
            button.config(image=button_image_2, state=tk.DISABLED, cursor=inactive_cursor)
            deactivate_hover(button)
        
        def check_previous_deactivate_button(button):
            """Vérifier quel bouton était désactivé avant de désactiver le bouton actuel.

            Args:
                button (Any): le bouton à réactiver.
            """        
            global Chromedriver_clicked, Update_clicked, Download_clicked

            def deactivate_chromedriver_page():
                """Masquer les éléments de la page Chromedriver
                """
                global Chromedriver_window 
                        
                activate_button(button_1,chromedriver_page_1,chromedriver_page_2)
                hide_text(chromedriver_path,chromedriver_path_info,chromedriver_mode,chromedriver_checkbox_info_1,chromedriver_checkbox_info_2)
                mask_elements(chromedriver_entry,chromedriver_checkbox,choose_file_path)
                Chromedriver_window = True
            
            def deactivate_update_page():
                """Masquer les éléments de la page Update
                """
                global Update_window

                activate_button(button_2,update_page_1,update_page_2)
                hide_text(update_mode, update_mode_info_1, update_mode_info_2, update_websites, update_websites_info, update_scantrad, update_lelscan, update_fmteam)
                mask_elements(update_entry, update_checkbox_1, update_checkbox_2, update_checkbox_3)
                Update_window = True

            def deactivate_download_page():
                """Masquer les éléments de la page Download
                """
                global Download_window

                activate_button(button_3,download_page_1,download_page_2)
                hide_text(download_path, download_path_info)
                mask_elements(download_entry, choose_directory_path)
                Download_window = True

            if button == button_1:                                                                  # Chromedriver
                deactivate_button(button,chromedriver_page_2)
                Chromedriver_clicked += 1
                if Update_window == False:
                    deactivate_update_page()
                elif Download_window == False:
                    deactivate_download_page()
            elif button == button_2:                                                                # Update
                deactivate_button(button,update_page_2)
                Update_clicked += 1
                if Download_window == False:
                    deactivate_download_page()
                elif Chromedriver_window == False:
                    deactivate_chromedriver_page()
            elif button == button_3:                                                               # Download
                deactivate_button(button,download_page_2)
                Download_clicked += 1
                if Chromedriver_window == False:
                    deactivate_chromedriver_page()
                elif Update_window == False:
                    deactivate_update_page()
            
        def chromedriver_settings():
            """ Actions lorsque le bouton chromedriver est cliqué.
            """
            global Chromedriver_window, Chromedriver_clicked, chromedriver_path, chromedriver_entry, choose_file_path, chromedriver_path_info, chromedriver_mode, chromedriver_checkbox, chromedriver_checkbox_info_1, chromedriver_checkbox_info_2

            Chromedriver_window = False

            if Chromedriver_clicked != 0:
                check_previous_deactivate_button(button_1)
                show_elements(button_1)
                show_text(chromedriver_path, chromedriver_path_info, chromedriver_mode, chromedriver_checkbox_info_1, chromedriver_checkbox_info_2)
                return

            # [ TEXT ]   Path*
            chromedriver_path = canvas.create_text(49.0, 75.0, anchor="nw", text="Path*", fill=current_color, font=title_police)
            # [ WIDGET ] Entry
            chromedriver_entry = tk.Entry(settings_window, bd=0, bg=current_color, fg=entry_textcolor, highlightthickness=0)
            chromedriver_entry.insert(0, config["chromedriver_path"])
            chromedriver_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
            # [ WIDGET ] Button choose file
            choose_file_path = tk.Button(settings_window, cursor=active_cursor, width=0, height=0, bd=0, text="Search", font=corpus_police, command=lambda:choose_file(chromedriver_entry))
            choose_file_path.configure(highlightbackground=background_button_color)
            choose_file_path.place(x=340.0, y=70.0, width=50.0, height=25.0)
            # [ TEXT ]   Info path
            chromedriver_path_info = canvas.create_text(93.0, 95.0, anchor="nw", text="The path to your automated browser 🤖[EXE]", fill=current_color, font=info_police)
            # [ TEXT ]   Mode chromedriver
            chromedriver_mode = canvas.create_text(49.0, 110.0, anchor="nw", text="Mode", fill=current_color, font=title_police)
            # [ WIDGET ] Checkbox
            chromedriver_checkbox = tk.Checkbutton(settings_window, variable=chromedriver_mode_var, cursor=active_cursor, width=0, height=0, bd=0, bg=current_color, justify="left", highlightthickness=0)
            chromedriver_checkbox.place(x=93.0, y=113.0, width=14.0, height=12.0)
            # [ TEXT ]   Infos checkbox
            chromedriver_checkbox_info_1 = canvas.create_text(93.0, 130.0, anchor="nw", text="Checked ( Default ): you can’t see the automated browser", fill=current_color,font=info_police)
            chromedriver_checkbox_info_2 = canvas.create_text(93.0, 142.0, anchor="nw", text="Unchecked : you can see the automated browser", fill=alt_color, font=info_police)

            Chromedriver_clicked = 1

        def update_settings():
            """ Actions lorsque le bouton update est cliqué.
            """
            global Update_window, Update_clicked, update_mode, update_entry, update_mode_info_1, update_mode_info_2, update_websites, update_websites_info, update_scantrad, update_checkbox_1, update_lelscan, update_checkbox_2, update_fmteam, update_checkbox_3

            Update_window = False

            if Update_clicked != 0:
                check_previous_deactivate_button(button_2)
                show_elements(button_2)
                show_text(update_mode, update_mode_info_1, update_mode_info_2, update_websites, update_websites_info, update_scantrad, update_lelscan, update_fmteam)
                return

            check_previous_deactivate_button(button_2)
            
            # [ TEXT ]   Mode update
            update_mode = canvas.create_text(49.0, 75.0, anchor="nw", text="Mode", fill=current_color, font=title_police)
            # [ WIDGET ] Entry
            update_entry = tk.Entry(settings_window, bd=0, bg=current_color, fg=entry_textcolor, highlightthickness=0)
            update_entry.insert(0, config["Update"]["mode"])
            update_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
            # [ TEXT ]   Infos mode
            update_mode_info_1 = canvas.create_text(93.0, 96.0, anchor="nw", text="'Manual' ( Default ) : Manually launch the update for a specific website.", fill=current_color, font=info_police)
            update_mode_info_2 = canvas.create_text(93.0, 108.0, anchor="nw", text="'Auto' : App automatically update datas at every launch", fill=alt_color, font=info_police)
            # [ TEXT ]   Websites
            update_websites = canvas.create_text(49.0, 125.0, anchor="nw", text="Websites", fill=current_color, font=title_police)
            # [ TEXT ]   Info websites
            update_websites_info = canvas.create_text(50.0, 140.0, anchor="nw", text="Enable [Checked] or Disable [Unchecked] any website’s Update.", fill=current_color, font=info_police)
            # [ TEXT ]   Scantrad
            update_scantrad = canvas.create_text(65.0, 158.0, anchor="nw", text="Scantrad", fill=current_color, font=corpus_police)
            # [ WIDGET ] Checkbox_1
            update_checkbox_1 = tk.Checkbutton(settings_window, variable=scantrad_checkbox_var, cursor=active_cursor, width=0, height=0, bd=0, bg=current_color, justify="left", highlightthickness=0)
            update_checkbox_1.place(x=118.0, y=158.0, width=14.0, height=12.0)
            # [ TEXT ]   Lelscan
            update_lelscan = canvas.create_text(65.0, 176.0, anchor="nw", text="Lelscans", fill=current_color, font=corpus_police)
            # [ WIDGET ] Checkbox_2
            update_checkbox_2 = tk.Checkbutton(settings_window, variable=lelscans_checkbox_var, cursor=active_cursor, width=0, height=0, bd=0, bg=current_color, justify="left", highlightthickness=0)
            update_checkbox_2.place(x=118.0, y=176.0, width=14.0, height=12.0)
            # [ TEXT ]   Fmteam
            update_fmteam = canvas.create_text(65.0, 196.0, anchor="nw", text="Fmteam", fill=current_color, font=corpus_police)
            # [ WIDGET ] Checkbox_3
            update_checkbox_3 = tk.Checkbutton(settings_window, variable=fmteam_checkbox_var, cursor=active_cursor, width=0, height=0, bd=0, bg=current_color, justify="left", highlightthickness=0)
            update_checkbox_3.place(x=118.0, y=196.0, width=14.0, height=12.0)
        
        def download_settings():
            """ Actions lorsque le bouton download est cliqué.
            """
            global Download_window, Download_clicked, download_path, download_entry, choose_directory_path, download_path_info

            Download_window = False

            if Download_clicked != 0:
                check_previous_deactivate_button(button_3)
                show_elements(button_3)
                show_text(download_path, download_path_info)
                return
            
            check_previous_deactivate_button(button_3)
            
            # [ TEXT ]   Path
            download_path = canvas.create_text(55.0, 77.0, anchor="nw", text="Path",  fill=current_color, font=title_police)
            # [ WIDGET ] Entry
            download_entry = tk.Entry(settings_window, bd=0, bg=current_color, fg=entry_textcolor, highlightthickness=0)
            download_entry.insert(0, config["Download"]["path"])
            download_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
            # [ WIDGET ] Button choose directory
            choose_directory_path = tk.Button(settings_window, cursor=active_cursor, width=0, height=0, bd=0, text="Search", font=corpus_police, command=lambda:choose_directory(download_entry))
            choose_directory_path.configure(highlightbackground=background_button_color)
            choose_directory_path.place(x=340.0, y=70.0, width=50.0, height=25.0)
            # [ TEXT ]   Info path
            download_path_info = canvas.create_text(55.0, 100.0, anchor="nw", text="The directory path where you want your files to be stored. ( Default : PandaScan 🐼 directory )", fill=current_color, font=info_police)
        
        def save_settings():
            """ Actions lorsque le bouton save est cliqué.
            """
            global save_clicked

            save_confirm = messagebox.askquestion(message=f" Save new settings ❓ ")

            if save_confirm == "yes":
                config["chromedriver_path"] = chromedriver_entry.get()
                config["driver"]["headless"] = chromedriver_mode_var.get()
                config["Update"]["mode"] = update_entry.get() 
                config["websites"]["fmteam.fr"]["enabled"] = fmteam_checkbox_var.get()
                config["websites"]["lelscans.net"]["enabled"] = lelscans_checkbox_var.get()
                config["websites"]["scantrad-vf"]["enabled"] = scantrad_checkbox_var.get()
                config["Download"]["path"] = download_entry.get()
                
                with open('config.json', 'w') as json_file:
                    json.dump(config, json_file, indent=4)

                save_clicked += 1

                return print("\nSettings saved ✅")
            
            else:

                save_clicked = 0
                return print("\nSaving canceled ❌")

        # ============================================================================================================================================================================================================================

        ################################ Basic Elements ##################################

        # ===== Background =====
        background = PhotoImage(file=relative_to_assets("background.png"))
        image_1 = canvas.create_image(241.0, 159.0, image=background)

        # ===== app logo =====
        app_logo_m = PhotoImage(file=relative_to_assets("app_logo_m.png"))
        image_2 = canvas.create_image(449.0, 23.0, image=app_logo_m)

        # ===== foreground =====
        foreground = PhotoImage(file=relative_to_assets("foreground.png"))
        image_3 = canvas.create_image(241.0, 179.0, image=foreground)

        ################################### Buttons ####################################### 

        # ================================================================================================ Chromedriver
        chromedriver_page_2 = PhotoImage(file=relative_to_assets("chromedriver_page_2.png"))
        chromedriver_page_1 = PhotoImage(file=relative_to_assets("chromedriver_page_1.png"))
        button_1 = tk.Button(
            settings_window,
            image=chromedriver_page_2,
            borderwidth=0,
            highlightthickness=0,
            command=chromedriver_settings,
            relief="flat",
            state=tk.DISABLED,
            cursor=inactive_cursor
        )
        button_1.place(x=29, y=23, width=108, height=28)
        
        # ================================================================================================ Update
        update_page_2 = PhotoImage(file=relative_to_assets("update_page_2.png"))
        update_page_1 = PhotoImage(file=relative_to_assets("update_page_1.png"))
        button_2 = tk.Button(
            settings_window,
            image=update_page_1,
            borderwidth=0,
            highlightthickness=0,
            command=update_settings,
            relief="flat",
            state=tk.NORMAL,
            cursor=active_cursor
        )
        button_2.place(x=157, y=24, width=61, height=27)

        button_hover(button_2,update_page_1,update_page_2)
        # ================================================================================================ Download
        download_page_2 = PhotoImage(file=relative_to_assets("download_page_2.png"))
        download_page_1 = PhotoImage(file=relative_to_assets("download_page_1.png"))
        button_3 = tk.Button(
            settings_window,
            image=download_page_1,
            borderwidth=0,
            highlightthickness=0,
            command=download_settings,
            relief="flat",
            state=tk.NORMAL,
            cursor=active_cursor
        )
        button_3.place(x=237, y=23, width=80, height=28)

        button_hover(button_3,download_page_1,download_page_2)
        # ================================================================================================ Save
        save_button_2 = PhotoImage(file=relative_to_assets("save_button_2.png"))
        save_button_1 = PhotoImage(file=relative_to_assets("save_button_1.png"))
        button_4 = tk.Button(
            settings_window,
            image=save_button_1,
            borderwidth=0,
            highlightthickness=0,
            command=save_settings,
            relief="flat",
            state=tk.NORMAL,
            cursor=active_cursor
        )
        button_4.place(x=210, y=271, width=91, height=25)
        
        button_hover(button_4,save_button_1,save_button_2)  
        ##############################################################################################################

        chromedriver_settings()                                          # Afficher les paramètres de la première page ( chromedriver par défaut )
        # charger les éléments des pages update et download
        update_settings()
        download_settings()
        # retourner à la page chromedriver par défaut
        chromedriver_settings()                                          
        settings_window.protocol("WM_DELETE_WINDOW", on_closing)         # Lier la fonction "on_closing" à la fermeture de l'application
        settings_window.resizable(False, False)                          # Restreindre le redimensionnement de la fenêtre
        settings_window.mainloop()                                       # Afficher la fenêtre

    else:
        settings_window.deiconify()

    #####################################################################################################################################
