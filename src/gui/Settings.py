import tkinter.filedialog as filedialog
import json
import os
import tkinter as tk
from tkinter import Toplevel, BooleanVar, Entry, Button, OptionMenu
from tkinter import Checkbutton, Canvas, PhotoImage, messagebox, StringVar
from .utils import button_hover, activate_button, deactivate_button, manage_menu
from src.foundation.selenium.utils import check_path
from src.foundation.core.essentials import relative_to_assets
from src.foundation.core.essentials import INACTIVE_CURSOR, ACTIVE_CURSOR
from src.foundation.core.essentials import OS_NAME, PATH_TO_CONFIG, LOG
from src.foundation.core.emojis import EMOJIS


INFO_POLICE = ("Inter", 8 * -1)          # INFOS font
TITLE_POLICE = ("Inter Bold", 12 * -1)   # TITLES -||-
CORPUS_POLICE = ("Inter Bold", 10 * -1)  # Alternative titles -||-
CURRENT_COLOR = "#FFFFFF"                # Dominant color (white)
ALT_COLOR = "#FFC700"                    # Alternative INFOS -||-
ENTRY_TEXT_COLOR = "#000716"             # Text entry -||-
BACKGROUND_BUTTON_COLOR = "red"          # Background buttons -||-
FR_WEBSITES_COLOR = "#0031AF"            # French websites -||-
EN_WEBSITES_COLOR = "#640000"            # English websites -||-

settings_window = None                  # State of the SETTINGS window
chromedriver_button_state = False       # State of the CHROMEDRIVER button
update_button_state = True              # -||- UPDATE button
download_button_state = True            # -||- DOWNLOAD button
chromedriver_clicks = 0                 # Number of clicks on the CHROMEDRIVER button
update_clicks = 0                       # -||- UPDATE button
download_clicks = 0                     # -||- DOWNLOAD button
save_clicks = 0                         # -||- SAVE button

# CHROMEDRIVER_PAGE
TEXT_1 = "Path*"
TEXT_2 = f"Path to your automated browser {EMOJIS[18]}"
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
TEXT_15 = "Lelmanga"
TEXT_16 = "Mangamoins"
TEXT_17 = "Tcbscans"
TEXT_18 = "Manganelo"
TEXT_19 = "Mangasaki"
# DOWNLOAD_PAGE
TEXT_50 = "Path"
TEXT_51 = f"The folder where your scans'll be stored. ( Default : PandaScan {EMOJIS[0]} directory )"
# Choose Button
TEXT_100 = "Choose"

def show_settings(main_window, SETTINGS, settings_button):
    """Display the SETTINGS window.

    Args:
        main_window (Any): master window
        SETTINGS (Any): .json file
        settings_button (Any): attached button
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

        # Store checkboxes states
        chromedriver_mode_var = BooleanVar(value=SETTINGS["driver"]["headless"])
        fmteam_checkbox_var = BooleanVar(value=SETTINGS["websites"]["fmteam"]["enabled"])
        lelscans_checkbox_var = BooleanVar(value=SETTINGS["websites"]["lelscans"]["enabled"])
        scantrad_checkbox_var = BooleanVar(value=SETTINGS["websites"]["scantrad"]["enabled"])
        animesama_checkbox_var = BooleanVar(value=SETTINGS["websites"]["animesama"]["enabled"])
        lelmanga_checkbox_var = BooleanVar(value=SETTINGS["websites"]["lelmanga"]["enabled"])
        tcbscans_checkbox_var = BooleanVar(value=SETTINGS["websites"]["tcbscans"]["enabled"])
        manganelo_checkbox_var = BooleanVar(value=SETTINGS["websites"]["manganelo"]["enabled"])
        mangamoins_checkbox_var = BooleanVar(value=SETTINGS["websites"]["mangamoins"]["enabled"])
        mangasaki_checkbox_var = BooleanVar(value=SETTINGS["websites"]["mangasaki"]["enabled"])

        # Initialize dictionaries [widgets + labels]
        widgets_to_manage = {}
        labels_to_manage = {}

        # === FUNCTIONS

        def on_closing():
            """Tasks to perform when closing the window.
            """

            settings_button.config(state="normal")

            LOG.debug(f"Settings exited {EMOJIS[1]}")
            os.system("clear")
            if save_clicks == 0:
                LOG.info("\nNo changes in Settings.")
            else:
                LOG.info("\nThere are some changes in Settings, please restart your app.")

            settings_window.withdraw()

        def choose_directory(entry):
            """Choose a folder location.

            Args:
                entry (Any): Input for entering the chosen path.
            """
            directory = filedialog.askdirectory()
            entry.delete(0, tk.END)
            entry.insert(0, directory)

        def choose_file(entry):
            """Choose a file location.

            Args:
                entry (Any): Input for entering the chosen path.
            """
            file = filedialog.askopenfilename(title="select the chromedriver file")
            if file:
                entry.delete(0, tk.END)
                entry.insert(0, file)

        def mask_elements(button):
            """Hide one or more widgets.

            Args:
                button: the widget button
            """
            for element in widgets_to_manage[button].keys():
                element.place_forget()

        def hide_text(button):
            """Hide one or more textual elements.

            Args:
                button (Any): the widget button
            """
            for element in labels_to_manage[button].keys():
                canvas.itemconfig(element, state="hidden")

        def show_text(button):
            """Display one or more textual elements.

            Args:
                button (Any): the widget button
            """
            for element in labels_to_manage[button].keys():
                canvas.itemconfig(element, state="normal")

        def show_elements(button):
            """Display the hidden widgets.

            Args:
                button (Any): the widget button
            """
            for element, (x, y, width, height) in widgets_to_manage[button].items():
                element.place(x=x, y=y, width=width, height=height)
            settings_window.update()

        def Switch_update_mode(*args):
            manage_menu(update_mode_menu, ["manual", "auto"], update_mode_var)

        def check_previous_deactivate_button(button):
            """Check which button was disabled before disabling the current button.

            Args:
                button (Any): the widget button
            """
            global chromedriver_clicks, chromedriver_button_state, update_clicks, update_button_state, download_clicks, download_button_state

            def manage_page_deactivation(button, button_image_1, button_image_2, window_state):
                """Masquer les éléments de la page correspondante

                Args:
                    button (Any): the widget button
                    button_image_1 (Any): default image
                    button_image_2 (Any): alternative image
                    window_state (Any): window state

                Returns:
                    bool: True(window is inactive) , False(otherwise)
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
            """Manage the display of a page.

            Args:
                button (Any): the widget button
            """
            check_previous_deactivate_button(button)
            show_elements(button)
            show_text(button)

        def chromedriver_settings():
            """Load the elements of the Chromedriver page.
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
            chromedriver_entry.insert(0, SETTINGS["driver"]["path"])
            chromedriver_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
            # [ WIDGET ] Button choose file
            choose_file_path = Button(settings_window, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, text=TEXT_100, font=CORPUS_POLICE, command=lambda: choose_file(chromedriver_entry))
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

            # Widgets to manage
            widgets_to_manage[button_1] = {
                chromedriver_entry: (92.0, 76.0, 228.0, 13.0),
                choose_file_path: (340.0, 70.0, 50.0, 25.0),
                chromedriver_checkbox: (93.0, 113.0, 14.0, 12.0)
            }
            # Labels to manage
            labels_to_manage[button_1] = {
                chromedriver_path: (49.0, 75.0),
                chromedriver_path_info: (93.0, 95.0),
                chromedriver_mode: (49.0, 110.0),
                chromedriver_checkbox_info_1: (93.0, 130.0),
                chromedriver_checkbox_info_2: (93.0, 142.0)
            }

            chromedriver_clicks = 1

        def update_settings():
            """Load the elements of the Update page.
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
            update_mode_menu = OptionMenu(settings_window, update_mode_var, update_mode_var.get())
            manage_menu(update_mode_menu, ["manual", "auto"], update_mode_var)
            update_mode_var.trace_add("write", Switch_update_mode)
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
            update_scantrad = canvas.create_text(65.0, 158.0, anchor="nw", text=TEXT_11, fill=FR_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_1 [Scantrad]
            update_checkbox_1 = Checkbutton(settings_window, variable=scantrad_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_1.place(x=125.0, y=158.0, width=14.0, height=12.0)
            # [ TEXT ]   Lelscans
            update_lelscan = canvas.create_text(65.0, 176.0, anchor="nw", text=TEXT_12, fill=FR_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_2 [Lelscan]
            update_checkbox_2 = Checkbutton(settings_window, variable=lelscans_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_2.place(x=125.0, y=176.0, width=14.0, height=12.0)
            # [ TEXT ]   Fmteam
            update_fmteam = canvas.create_text(65.0, 196.0, anchor="nw", text=TEXT_13, fill=FR_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_3 [Fmteam]
            update_checkbox_3 = Checkbutton(settings_window, variable=fmteam_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_3.place(x=125.0, y=196.0, width=14.0, height=12.0)
            # [ TEXT ]   Animesama
            update_animesama = canvas.create_text(65.0, 216.0, anchor="nw", text=TEXT_14, fill=FR_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_4 [Animesama]
            update_checkbox_4 = Checkbutton(settings_window, variable=animesama_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_4.place(x=125.0, y=216.0, width=14.0, height=12.0)
            # [ TEXT ]   Lelmanga
            update_lelmanga = canvas.create_text(65.0, 236.0, anchor="nw", text=TEXT_15, fill=FR_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_5 [Lelmanga]
            update_checkbox_5 = Checkbutton(settings_window, variable=lelmanga_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_5.place(x=125.0, y=236.0, width=14.0, height=12.0)
            # [ TEXT ]   Mangamoins
            update_mangamoins = canvas.create_text(195.0, 158.0, anchor="nw", text=TEXT_16, fill=FR_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_6 [Mangamoins]
            update_checkbox_6 = Checkbutton(settings_window, variable=mangamoins_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_6.place(x=265.0, y=158.0, width=14.0, height=12.0)
            # [ TEXT ]   Tcbscans
            update_tcbscans = canvas.create_text(195.0, 176.0, anchor="nw", text=TEXT_17, fill=EN_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_7 [Tcbscans]
            update_checkbox_7 = Checkbutton(settings_window, variable=tcbscans_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_7.place(x=265.0, y=176.0, width=14.0, height=12.0)
            # [ TEXT ]   Manganelo
            update_manganelo = canvas.create_text(195.0, 196.0, anchor="nw", text=TEXT_18, fill=EN_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_8 [Manganelo]
            update_checkbox_8 = Checkbutton(settings_window, variable=manganelo_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_8.place(x=265.0, y=196.0, width=14.0, height=12.0)
            # [ TEXT ]   Mangasaki
            update_mangasaki = canvas.create_text(195.0, 216.0, anchor="nw", text=TEXT_19, fill=EN_WEBSITES_COLOR, font=CORPUS_POLICE)
            # [ WIDGET ] Checkbox_9 [Mangasaki]
            update_checkbox_9 = Checkbutton(settings_window, variable=mangasaki_checkbox_var, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, bg=CURRENT_COLOR, justify="left", highlightthickness=0)
            update_checkbox_9.place(x=265.0, y=216.0, width=14.0, height=12.0)

            # Widgets to manage
            widgets_to_manage[button_2] = {
                update_mode_menu: (92.0, 76.0, 80, 15.0),
                update_checkbox_1: (125.0, 158.0, 14.0, 12.0),
                update_checkbox_2: (125.0, 176.0, 14.0, 12.0),
                update_checkbox_3: (125.0, 196.0, 14.0, 12.0),
                update_checkbox_4: (125.0, 216.0, 14.0, 12.0),
                update_checkbox_5: (125.0, 236.0, 14.0, 12.0),
                update_checkbox_6: (265.0, 158.0, 14.0, 12.0),
                update_checkbox_7: (265.0, 176.0, 14.0, 12.0),
                update_checkbox_8: (265.0, 196.0, 14.0, 12.0),
                update_checkbox_9: (265.0, 216.0, 14.0, 12.0)}
            # Labels to manage
            labels_to_manage[button_2] = {
                update_mode: (49.0, 75.0),
                update_mode_info_1: (93.0, 96.0),
                update_mode_info_2: (93.0, 108.0),
                update_websites: (49.0, 125.0),
                update_websites_info: (50.0, 140.0),
                update_scantrad: (65.0, 158.0),
                update_lelscan: (65.0, 176.0),
                update_fmteam: (65.0, 196.0),
                update_animesama: (65.0, 216.0),
                update_lelmanga: (65.0, 236.0),
                update_mangamoins: (195.0, 158.0),
                update_tcbscans: (195.0, 176.0),
                update_manganelo: (195.0, 196.0),
                update_mangasaki: (195.0, 216.0)}

            check_previous_deactivate_button(button_2)

        def download_settings():
            """Load the elements of the Download page.
            """
            global download_button_state, download_clicks
            global download_entry, choose_directory_path
            global download_path, download_path_info

            download_button_state = False

            if download_clicks != 0:
                manage_window(button_3)
                return

            # [ TEXT ]   Path
            download_path = canvas.create_text(55.0, 75.0, anchor="nw", text=TEXT_50, fill=CURRENT_COLOR, font=TITLE_POLICE)
            # [ WIDGET ] Entry
            download_entry = Entry(settings_window, bd=0, bg=CURRENT_COLOR, fg=ENTRY_TEXT_COLOR, highlightthickness=0)
            download_entry.insert(0, SETTINGS["Download"]["path"])
            download_entry.place(x=92.0, y=76.0, width=228.0, height=13.0)
            # [ WIDGET ] Choose directory button
            choose_directory_path = Button(settings_window, cursor=ACTIVE_CURSOR, width=0, height=0, bd=0, text=TEXT_100, font=CORPUS_POLICE, command=lambda: choose_directory(download_entry))
            choose_directory_path.configure(highlightbackground=BACKGROUND_BUTTON_COLOR)
            choose_directory_path.place(x=340.0, y=70.0, width=50.0, height=25.0)
            # [ TEXT ]   Info path
            download_path_info = canvas.create_text(55.0, 100.0, anchor="nw", text=TEXT_51, fill=CURRENT_COLOR, font=INFO_POLICE)

            # Widgets to manage
            widgets_to_manage[button_3] = {
                download_entry: (92.0, 76.0, 228.0, 13.0),
                choose_directory_path: (340.0, 70.0, 50.0, 25.0)}
            # Labels to manage
            labels_to_manage[button_3] = {
                download_path: (55.0, 75.0),
                download_path_info: (55.0, 100.0)}

            check_previous_deactivate_button(button_3)

        def save_settings():
            """Save the changes to the config file.
            """
            global save_clicks

            save_confirm = messagebox.askquestion(message=f"Save new settings {EMOJIS[19]}")

            if save_confirm == "yes":
                SETTINGS["driver"]["path"] = check_path(OS_NAME, LOG, chromedriver_entry.get())
                SETTINGS["driver"]["headless"] = chromedriver_mode_var.get()
                SETTINGS["Update"]["mode"] = update_mode_var.get()
                SETTINGS["websites"]["fmteam"]["enabled"] = fmteam_checkbox_var.get()
                SETTINGS["websites"]["lelscans"]["enabled"] = lelscans_checkbox_var.get()
                SETTINGS["websites"]["scantrad"]["enabled"] = scantrad_checkbox_var.get()
                SETTINGS["websites"]["animesama"]["enabled"] = animesama_checkbox_var.get()
                SETTINGS["websites"]["lelmanga"]["enabled"] = lelmanga_checkbox_var.get()
                SETTINGS["websites"]["tcbscans"]["enabled"] = tcbscans_checkbox_var.get()
                SETTINGS["websites"]["manganelo"]["enabled"] = manganelo_checkbox_var.get()
                SETTINGS["websites"]["mangamoins"]["enabled"] = mangamoins_checkbox_var.get()
                SETTINGS["websites"]["mangasaki"]["enabled"] = mangasaki_checkbox_var.get()
                SETTINGS["Download"]["path"] = check_path(OS_NAME, LOG, download_entry.get())

                with open(PATH_TO_CONFIG, 'w') as json_file:
                    json.dump(SETTINGS, json_file, indent=4)

                save_clicks += 1

                return LOG.debug(f"New settings saved {EMOJIS[3]}")

            else:

                save_clicks = 0
                return LOG.debug(f"Saving canceled {EMOJIS[4]}")

        # === APP FOUNDATIONS

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
