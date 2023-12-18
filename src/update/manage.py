import time
import os
from tkinter import messagebox
from src.migrate.manage import Manage_migration
from .utils import confirm_update, check_and_update
from src.foundation.core.emojis import EMOJIS


def manual_update(SRC_DIRECTORY, selected_website, SETTINGS, CONN, SELECTOR, WEBSITES, LOG):
    """Launch manual update of a website.

    Args:
        SRC_DIRECTORY (str): path to the src directory
        selected_website (str): name of the website to update
        SETTINGS (Any): .json configuration file
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
        WEBSITES (dict): list of available websites
        LOG (Any): the logger
    """

    i = 0
    mode = "Manual"
    message = selected_website

    if confirm_update(mode, message):
        os.system("clear")
        LOG.info(f"Searching for {selected_website} Updates {EMOJIS[8]}..")

        start_time = time.time()
        i, website_status = check_and_update(selected_website, SETTINGS, i, LOG)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if i != 0:
            LOG.info(f"{selected_website} is Up-to-date {EMOJIS[3]} | lasted: {elapsed_time:.2f} s")

            result = Manage_migration(SRC_DIRECTORY, CONN, SELECTOR, WEBSITES, LOG)
            if result == "success":
                LOG.info(f"Migration completed {EMOJIS[3]}.")
                messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"Update completed {EMOJIS[3]}\n Explore the changelogs {EMOJIS[16]}")
            elif result == "failed":
                LOG.info(f"Migration failed {EMOJIS[4]}.")
                messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"Update failed {EMOJIS[4]}\n Please Debug {EMOJIS[10]}")
        else:
            messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"Update failed {EMOJIS[4]}")
    else:
        LOG.debug(f"{mode} Update Canceled")


def auto_update(SRC_DIRECTORY, WEBSITES, SETTINGS, CONN, SELECTOR, LOG):
    """Launch auto update of websites.

    Args:
        SRC_DIRECTORY (str): path to the src directory
        WEBSITES (dict): list of available websites
        SETTINGS (Any): .json configuration file
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
        LOG (Any): the logger
    """

    i = 0
    mode = "Auto"
    message = "all websites"

    if confirm_update(mode, message):
        os.system("clear")
        LOG.info(f"Searching for Updates {EMOJIS[8]}..")

        for website in WEBSITES:

            start_time = time.time()
            i, website_status = check_and_update(website, SETTINGS, i, LOG)
            i += i
            end_time = time.time()
            elapsed_time = end_time - start_time
            if website_status is True and i != 0:
                LOG.info(f"{website} is Up-to-date {EMOJIS[3]} | lasted: {elapsed_time:.2f} s")
            else:
                LOG.info(f"{website} Update failed {EMOJIS[4]} | lasted: {elapsed_time:.2f} s")

        if i != 0:
            result = Manage_migration(SRC_DIRECTORY, CONN, SELECTOR, WEBSITES, LOG)
            if result == "success":
                LOG.info(f"Migration completed {EMOJIS[3]}.")
                messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"Update completed {EMOJIS[3]}\n Explore the changelogs {EMOJIS[16]}")
            elif result == "failed":
                LOG.info(f"Migration failed {EMOJIS[4]}.")
                messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"Update failed {EMOJIS[4]}\n Please Debug {EMOJIS[10]}")

    else:
        LOG.debug(f"{mode} Update Canceled")
