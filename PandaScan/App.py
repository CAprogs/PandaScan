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
# This project aims to download mangas scans with ease for local access and private use.
# For now, Chromedriver is required to use PandaScan. Please follow the 'README' file for more information.
# You are now able to change Settings directly in App.
#    ° Choose between "manual" or "auto" update.
#    ° Select where to save your scans after a download.
#    ° Updating PandaScan generates changelog files | Check changelogs in 'changelog > choose a website > changelog.txt'.
# Please note that some websites may provide empty folders when downloading (especially scantrad)
# If you like this project, please consider giving it a ⭐️ on Github.🫶
# Credits: @Tkinter-designer by ParthJadhav
# ------------------------------------------------------------------------------------------------------------


import os
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Listbox, IntVar
from tkinter import Scrollbar, Button, Checkbutton
from tkinter import PhotoImage, StringVar, OptionMenu, messagebox
from foundation.tracker.progessbar import ProgressBar
from download.manage import download
from update.manage import manual_update, auto_update
from gui.Settings import show_settings
from gui.utils import button_hover
from foundation.core.essentials import relative_to_assets, check_connection
from foundation.core.essentials import INACTIVE_CURSOR, ACTIVE_CURSOR, CONN, SELECTOR
from foundation.core.essentials import MAIN_DIRECTORY, DRIVER, SETTINGS, LOG
from foundation.core.essentials import WEBSITES, ALL_WEBSITES, FR_WEBSITES, EN_WEBSITES
from foundation.core.emojis import EMOJIS


POLICE_1 = ("Inter", 15 * -1)
POLICE_2 = ("Inter", 16 * -1)
POLICE_3 = ("Inter", 12 * -1)
CURRENT_COLOR = "#FFFFFF"                     # dominant text color
ALT_COLOR = "#6B0000"                         # -||- info text color
ENTRY_TEXT_COLOR = "#000716"                  # -||- entry text color

default_website = WEBSITES[0]                 # website selected
nb_of_manga_chapters = 0                      # number of chapters from a manga (total)
nb_of_chapters_to_download = 0                # number of chapters to download
download_id = 0                               # id of the current download
downloads_succeeded = 0                       # number of succeeded downloads
downloads_failed = 0                          # number of failed downloads
downloads_skipped = 0                         # number of skipped downloads
selected_manga_name = ''                      # name of the selected manga
selected_manga_chapters = []                  # list that contains the selected chapters
start_index = ""                              # index associated to the first chapter of a range
end_index = ""                                # index associated to the last chapter of a range
download_button_state = False                 # state of the download button
manga_file_path = ''                          # path to the manga folder

TEXT_1 = EMOJIS[5]
TEXT_2 = "Manga name"
TEXT_3 = "Chapter / Volume"
TEXT_4 = "-"


def main():
    """Load application components."
    """

    if not check_connection():
        messagebox.showinfo(f"Error [{EMOJIS[14]}]", f"{EMOJIS[9]} Oups, no internet connection detected {EMOJIS[11]}")
        return print(f"\nPandascan exited {EMOJIS[1]}\n")

    print(f"PandaScan is running {EMOJIS[3]}\n")

    main_window = Tk()

    logo = PhotoImage(file=relative_to_assets("pandacon.gif"))
    main_window.call('wm', 'iconphoto', main_window._w, logo)

    main_window.title(f"PandaScan {EMOJIS[0]}")

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
        """Tasks when closing the application.
        """
        if DRIVER:
            DRIVER.quit()
        CONN.close()
        main_window.destroy()
        os.system("clear")
        print(f"\nApp closed {EMOJIS[2]}\n")

    def Clear_range_menus():
        """Clear and reset the selection range dropdown menus.
        """
        min_chapter_menu['menu'].delete(0, 'end')
        max_chapter_menu['menu'].delete(0, 'end')
        Check_box_var.set(0)
        min_chapter_var.set(" ")
        max_chapter_var.set(" ")
        min_chapter_menu.configure(state="disabled")
        max_chapter_menu.configure(state="disabled")
        Check_box.configure(state="disabled")

    def Reload_page():
        """Reset app's widgets.
        """
        global selected_manga_name

        selected_manga_name = ''

        entry_1.delete(0, tk.END)
        canvas.itemconfigure(Chapter_selected, text='')
        canvas.itemconfigure(Manga_selected, text='')
        result_box.delete(0, tk.END)
        chapters_box.delete(0, tk.END)
        Clear_range_menus()

    def Switch_website(*args):
        """Change the website.
        """
        global default_website

        selected_item = website_list_var.get()
        default_website = selected_item
        LOG.debug(f"Website : {selected_item}")
        Reload_page()

    def Switch_language(*args):
        """Fetch the website's menu with the websites associated to the selected language.
        """

        if language_list_var.get() == "All":
            WEBSITES = ALL_WEBSITES
        elif language_list_var.get() == EMOJIS[6]:
            WEBSITES = FR_WEBSITES
        elif language_list_var.get() == EMOJIS[7]:
            WEBSITES = EN_WEBSITES

        website_menu['menu'].delete(0, 'end')
        website_list_var.set(WEBSITES[0])
        for website in WEBSITES:
            website_menu['menu'].add_command(label=website, command=tk._setit(website_list_var, website))
        LOG.debug(f"Websites displayed : {language_list_var.get()}")
        Reload_page()

    def update_results(event):
        """Update the results in the list of mangas.

        Args:
            event (Any): The event triggering the function.
        """
        keyword = entry_1.get()
        keyword = '%' + keyword + '%'
        query = "SELECT NomManga FROM Mangas WHERE NomManga LIKE ? AND NomSite = ?"
        SELECTOR.execute(query, (keyword, default_website))
        results = [row[0] for row in SELECTOR.fetchall()]
        result_box.delete(0, tk.END)
        result_box.insert(tk.END, *results)

    def on_mangas_select(event):
        """Actions when a manga is selected.

        Args:
            event (Any): The event triggering the function.
        """
        global selected_manga_name

        selected_indices = result_box.curselection()
        if selected_indices:
            selected_manga_name = result_box.get(selected_indices[0])
            update_chapters(selected_manga_name)
            truncated_text = selected_manga_name[:15] + "..." if len(selected_manga_name) > 15 else selected_manga_name
            canvas.itemconfigure(Manga_selected, text=truncated_text)

            result = chapters_box.get(tk.END)

            min_chapter_menu['menu'].delete(0, 'end')
            max_chapter_menu['menu'].delete(0, 'end')

            if result != "":
                fetch_chapters_in_menu()
            else:
                min_chapter_var.set(" ")
                max_chapter_var.set(" ")
                Check_box_var.set(0)
                min_chapter_menu.configure(state="disabled")
                max_chapter_menu.configure(state="disabled")
                Check_box.configure(state="disabled")

    def on_menu_select(*args):
        """Handle the re-selection of the chapter range.
        """
        if Check_box_var.get() == 1:
            chapters_box.selection_clear(0, tk.END)
            select_range()

    def fetch_chapters_in_menu():
        """Fill the list of chapters in the dropdown menus for range selection.
        """
        num_chapters = [chapitre.replace("chapitre ", "") for chapitre in chapters_box.get(0, tk.END)]
        for chapter in num_chapters:
            min_chapter_menu['menu'].add_command(label=chapter, command=tk._setit(min_chapter_var, chapter))
            max_chapter_menu['menu'].add_command(label=chapter, command=tk._setit(max_chapter_var, chapter))
        min_chapter_var.set(num_chapters[-1])
        max_chapter_var.set(num_chapters[0])
        min_chapter_menu.configure(state="normal")
        max_chapter_menu.configure(state="normal")
        Check_box.configure(state="normal")

    def select_range(*args):
        """Select a range of chapters.
        """
        global nb_of_manga_chapters, selected_manga_chapters, start_index, end_index

        if Check_box_var.get() == 1:

            min_var = min_chapter_var.get()
            max_var = max_chapter_var.get()
            start_chapter = "chapitre " + min_var
            end_chapter = "chapitre " + max_var

            all_chapters = chapters_box.get(0, tk.END)
            start_index = all_chapters.index(start_chapter)
            end_index = all_chapters.index(end_chapter)

            if float(max_var) < float(min_var):
                selected_range = chapters_box.get(start_index, end_index)
                LOG.debug(f"Selected range : from {start_chapter} to {end_chapter}")
            elif float(max_var) > float(min_var):
                selected_range = chapters_box.get(end_index, start_index)
                LOG.debug(f"Selected range : from {end_chapter} to {start_chapter}")
            else:
                selected_range = chapters_box.get(start_index, start_index)
                LOG.debug(f"You selected one chapter : {start_chapter}")

            chapters_box.select_set(start_index, end_index)
            selected_manga_chapters = selected_range
            nb_of_manga_chapters = len(selected_manga_chapters)
            canvas.itemconfigure(Chapter_selected, text=f'{nb_of_manga_chapters} selected')

        else:
            chapters_box.selection_clear(0, tk.END)
            selected_manga_chapters = []
            canvas.itemconfigure(Chapter_selected, text='0 selected')

    def update_chapters(selected_manga_name):
        """Update the results in the Chapter List when a manga is selected.

        Args:
            selected_manga_name (str): name of the selected manga
        """
        query = "SELECT Chapitres FROM Chapitres WHERE NomSite = ? AND NomManga = ?"
        SELECTOR.execute(query, (default_website, selected_manga_name))
        results = [result[0] for result in SELECTOR.fetchall()]
        chapters_box.delete(0, tk.END)
        chapters_box.insert(tk.END, *results)
        result = chapters_box.get(tk.END)
        if Check_box_var.get() == 1 or result != "":
            Clear_range_menus()

    def on_chapters_select(event):
        """Tasks when a chapter is selected.

        Args:
            event (Any): The event triggering the function.
        """
        global selected_manga_chapters, nb_of_manga_chapters

        selected_chapters = chapters_box.curselection()
        selected_manga_chapters = [chapters_box.get(index) for index in selected_chapters]
        nb_of_manga_chapters = len(selected_manga_chapters)
        canvas.itemconfigure(Chapter_selected, text=f'{nb_of_manga_chapters} selected')

    def Set_download():
        """Handle the download of selected chapters.
        """
        global download_id, downloads_succeeded, downloads_failed, downloads_skipped

        download_id = 0
        downloads_succeeded = 0
        downloads_failed = 0
        downloads_skipped = 0

        def Start_download(progress_bar):
            """Start the download of selected chapters.

            Args:
                progress_bar (Any): progress bar
            """
            global download_id, download_button_state, downloads_succeeded, downloads_failed, downloads_skipped

            chapter_name = selected_manga_chapters[download_id]
            if os.path.exists(SETTINGS['Download']['path']):
                chapter_file_path = manga_file_path + '/' + chapter_name
            else:
                chapter_file_path = manga_file_path / chapter_name

            status = download(default_website, chapter_file_path, selected_manga_name, download_id, chapter_name, manga_file_path, SETTINGS, SELECTOR)
            if status == "success":
                downloads_succeeded += 1
            elif status == "failed":
                downloads_failed += 1
            elif status == "skipped":
                downloads_skipped += 1

            download_id += 1
            if progress_bar is not None:
                progress_bar.update(download_id)
                progress_bar.display(prefix='Download', suffix=f'[{status}]')

            if download_id < nb_of_manga_chapters:
                main_window.after(100, Start_download(progress_bar))
            else:
                messagebox.showinfo(f"Download info [{EMOJIS[13]}]", f"""
                                    \nManga : {selected_manga_name}

                                    succeeded : {downloads_succeeded}/{nb_of_manga_chapters} {EMOJIS[3]}
                                    failed : {downloads_failed} {EMOJIS[4]}
                                    skipped : {downloads_skipped} {EMOJIS[12]}

                                    \nStored in : {manga_file_path}
                                    \n\nThanks for using PandaScan {EMOJIS[0]}""")
                download_button.configure(state="normal")
                download_button_state = False

        def Manage_download():
            """
            - Deactivate the download button
            - Instantiate a progress bar (INFO mode only)
            - Start the download of selected chapters
            """
            global download_button_state

            download_button_state = True
            download_button.configure(state="disabled")
            if SETTINGS['logger']['level'] == "INFO":
                progress_bar = ProgressBar(nb_of_manga_chapters)
            else:
                progress_bar = None
            Start_download(progress_bar)

        def Set_download_directory():
            """Handle the download directory.
            """
            global manga_file_path

            if os.path.exists(SETTINGS['Download']['path']):
                manga_file_path = SETTINGS['Download']['path'] + '/' + selected_manga_name
            else:
                manga_file_path = MAIN_DIRECTORY / selected_manga_name
                if not os.path.exists(manga_file_path):
                    os.makedirs(manga_file_path)
            Manage_download()

        if nb_of_manga_chapters == 0 or selected_manga_chapters == []:
            messagebox.showinfo(f"Info [{EMOJIS[13]}]", f"No Chapter Selected {EMOJIS[10]}, Try again")
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

    # === Manga search bar ( SearchBar )

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(510.5, 204.0, image=entry_image_1)
    entry_1 = Entry(main_window, bd=0, bg=CURRENT_COLOR, fg=ENTRY_TEXT_COLOR, highlightthickness=0)
    entry_1.place(x=376.0, y=195.0, width=269.0, height=16.0)

    # === Dropdown selection of the language preference

    language_list_var = StringVar(main_window)
    language_list_var.set(SETTINGS["websites"]["default"])
    language_menu = OptionMenu(main_window, language_list_var, "All", EMOJIS[6], EMOJIS[7])
    language_menu.place(x=420.0, y=150.0, width=47.0)
    language_menu.configure(bg=CURRENT_COLOR)
    language_list_var.trace_add("write", Switch_language)

    # === Dropdown selection of the website

    # canvas.create_text(413.0, 152.0, anchor="nw", text=TEXT_1, fill=CURRENT_COLOR, font=POLICE_1)
    website_list_var = StringVar(main_window)
    website_list_var.set(default_website)
    website_menu = OptionMenu(main_window, website_list_var, default_website)
    website_menu['menu'].delete(0, 'end')
    for website in WEBSITES:
        website_menu['menu'].add_command(label=website, command=tk._setit(website_list_var, website))
    website_menu.place(x=470.0, y=150.0)
    website_menu.configure(bg=CURRENT_COLOR)
    website_list_var.trace_add("write", Switch_website)

    # === ( ChapterBox : Image )

    Chapters_list_Box = PhotoImage(file=relative_to_assets("Chapters_list_Box.png"))
    canvas.create_image(588.0, 392.0, image=Chapters_list_Box)

    # === ( MangaBox : Image )

    Manga_name_listBox = PhotoImage(file=relative_to_assets("Manga_name_listBox.png"))
    canvas.create_image(382.0, 392.0, image=Manga_name_listBox)

    # === Manga Display area ( MangaBox )

    canvas.create_text(331.0, 269.0, anchor="nw", text=TEXT_2, fill=CURRENT_COLOR, font=POLICE_1)

    # Manga display list
    result_box = Listbox(main_window, selectmode=tk.SINGLE)
    result_box.place(x=306, y=300, width=150, height=190)
    # Scrollbar associated with the manga list
    result_scrollbar = Scrollbar(main_window)
    result_scrollbar.place(x=265, y=300, height=190)

    # Link the scrollbar to the manga list and vice versa
    result_scrollbar.config(command=result_box.yview)
    result_box.config(yscrollcommand=result_scrollbar.set, bd=0)

    # === Chapter Display area ( ChapterBox )

    canvas.create_text(525.0, 269.0, anchor="nw", text=TEXT_3, fill=CURRENT_COLOR, font=POLICE_1)

    # Chapter display list
    chapters_box = Listbox(main_window, selectmode=tk.MULTIPLE)
    chapters_box.place(x=535.0, y=300.0, width=100, height=190)
    # Scrollbar associated with the chapter list
    chapters_scrollbar = Scrollbar(main_window)

    # Link the scrollbar to the chapter list and vice versa
    chapters_scrollbar.config(command=chapters_box.yview)
    chapters_scrollbar.place(x=685, y=300, height=190)
    chapters_box.config(yscrollcommand=chapters_scrollbar.set, bd=0)

    # ===  Events associated to the widgets

    # Search the manga + Update the results
    entry_1.bind('<KeyRelease>', update_results)
    # Selection of the manga + display the name of the manga selected
    result_box.bind('<<ListboxSelect>>', on_mangas_select)
    # Selection of chapters + display the number of chapters selected
    chapters_box.bind('<<ListboxSelect>>', on_chapters_select)

    # === Select a range of chapters ( Menus + Checkbox )

    # 1st dropdown chapter menu
    min_chapter_var = StringVar(main_window)
    min_chapter_var.set(" ")
    min_chapter_menu = OptionMenu(main_window, min_chapter_var, "")
    min_chapter_menu.place(x=520.0, y=526.0, width=60.0, height=18.0)
    min_chapter_menu.configure(bg=CURRENT_COLOR, state="disabled")
    min_chapter_var.trace_add("write", lambda *args: on_menu_select())

    # "-" text
    canvas.create_text(585.0, 527.0, anchor="nw", text=TEXT_4, fill=ALT_COLOR, font=POLICE_3)

    # 2nd dropdown chapter menu
    max_chapter_var = StringVar(main_window)
    max_chapter_var.set(" ")
    max_chapter_menu = OptionMenu(main_window, max_chapter_var, "")
    max_chapter_menu.place(x=595.0, y=526.0, width=60.0, height=18.0)
    max_chapter_menu.configure(bg=CURRENT_COLOR, state="disabled")
    max_chapter_var.trace_add("write", lambda *args: on_menu_select())

    # validation checkbox
    Check_box_var = IntVar(main_window)
    Check_box = Checkbutton(main_window, variable=Check_box_var, command=select_range, bg="white", state="disabled")
    Check_box.place(x=655.0, y=524.0)

    # === Number of chapters selected ( Chapters_info Box )

    chapters_info_box = PhotoImage(file=relative_to_assets("Chapters_info.png"))
    canvas.create_image(588.0, 584.0, image=chapters_info_box)
    # Number of chapters selected
    Chapter_selected = canvas.create_text(550.0, 570.0, anchor="nw", text="", fill=ALT_COLOR, font=POLICE_2)

    # === Name of the selected manga ( Manga_info Box )

    Manga_name_info_box = PhotoImage(file=relative_to_assets("Manga_name_info.png"))
    canvas.create_image(381.0, 584.0, image=Manga_name_info_box)
    # Manga selected
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
        main_window.withdraw()
        update_button.config(state=tk.DISABLED, cursor=INACTIVE_CURSOR)
        auto_update(MAIN_DIRECTORY, WEBSITES, SETTINGS, CONN, SELECTOR, LOG)
        main_window.deiconify()
    elif SETTINGS['Update']['mode'] == "manual":
        update_button.config(command=lambda: manual_update(MAIN_DIRECTORY, default_website, SETTINGS, CONN, SELECTOR, WEBSITES, LOG))
        button_hover(update_button, button_update_1, button_update_2, download_button_state)

    main_window.protocol("WM_DELETE_WINDOW", on_closing)
    main_window.resizable(False, False)
    main_window.mainloop()


if __name__ == "__main__":
    main()
