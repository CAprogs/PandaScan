import time
import os
from tkinter import messagebox
from migrate.manage import Manage_migration
from .utils import confirm_update, check_and_update


def manual_update(MAIN_DIRECTORY, selected_website, SETTINGS, CONN, SELECTOR, WEBSITES, LOG):
    """Launch manual update of a website.

    Args:
        MAIN_DIRECTORY (str): path to the working directory
        selected_website (str): name of the website to update
        SETTINGS (Any): .json configuration file
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
        WEBSITES (dict): list of available websites
        LOG (Any): the logger
    """

    i = 0
    mode = "Manual"

    if confirm_update(mode):
        os.system("clear")
        LOG.info(f"Searching for {selected_website} Updates 🔄..")

        start_time = time.time()
        i = check_and_update(selected_website, SETTINGS, i, LOG)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if i != 0:
            LOG.info(f"{selected_website} is Up-to-date ✅ | lasted: {elapsed_time:.2f} s")

            Manage_migration(MAIN_DIRECTORY, CONN, SELECTOR, WEBSITES, LOG)
            messagebox.showinfo("Update Info ℹ️", "Update completed ✅\n Explore the changelogs 🔎")

    else:
        LOG.info(f"{mode} Update Canceled")


def auto_update(MAIN_DIRECTORY, WEBSITES, SETTINGS, CONN, SELECTOR, LOG):
    """Launch auto update of websites.

    Args:
        MAIN_DIRECTORY (str): path to the working directory
        WEBSITES (dict): list of available websites
        SETTINGS (Any): .json configuration file
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
        LOG (Any): the logger
    """

    i = 0
    mode = "Auto"

    if confirm_update(mode):
        os.system("clear")
        LOG.info("Searching for Updates 🔄..")

        for website in WEBSITES:

            start_time = time.time()
            i = check_and_update(website, SETTINGS, i, LOG)
            end_time = time.time()
            elapsed_time = end_time - start_time
            if i != 0:
                LOG.info(f"{website} is Up-to-date ✅ | lasted: {elapsed_time:.2f} s")

        if i != 0:
            Manage_migration(MAIN_DIRECTORY, CONN, SELECTOR, WEBSITES, LOG)
            messagebox.showinfo("Update Info ℹ️", "Update completed ✅\n Explore the changelogs 🔎")

    else:
        LOG.info(f"{mode} Update Canceled")
