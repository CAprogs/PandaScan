import time
import os
from tkinter import messagebox
from src.migrate.manage import Manage_migration
from .utils import confirm_update, check_and_update, w_average_time
from src.foundation.core.emojis import EMOJIS


def manual_update(SRC_DIRECTORY, selected_website, SETTINGS, CONN, SELECTOR, LOG):
    """Launch manual update of a website.

    Args:
        SRC_DIRECTORY (str): path to the src directory
        selected_website (str): name of the website to update
        SETTINGS (Any): .json configuration file
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
        LOG (Any): the logger
    """

    i = 0
    mode = "Manual"
    message = selected_website

    if confirm_update(mode, message, SETTINGS):
        os.system("clear")
        LOG.info(f"Searching for {selected_website} Updates {EMOJIS[8]}..")

        start_time = time.time()
        i, status = check_and_update(selected_website, SETTINGS, i, LOG)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if status == "success":
            LOG.info(f"{selected_website} is Up-to-date {EMOJIS[3]} | lasted: {elapsed_time:.2f} s")
            w_average_time(selected_website, round(elapsed_time, 2), SETTINGS)
            result = Manage_migration(SRC_DIRECTORY, CONN, SELECTOR, LOG)
            if result == "success":
                LOG.info(f"Migration completed {EMOJIS[3]}")
                messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"Migration completed {EMOJIS[3]}\n Explore the changelogs {EMOJIS[16]}")
            elif result == "failed":
                LOG.info(f"Migration failed {EMOJIS[4]}")
                messagebox.showinfo(f"Migration Info {EMOJIS[13]}", f"Migration failed {EMOJIS[4]}\n Please Debug {EMOJIS[10]}")

        elif status == "skipped":
            LOG.info(f"{selected_website} Update skipped {EMOJIS[12]}")
            messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"Sorry, {selected_website} can't be updated due to settings {EMOJIS[10]}")

        elif status == "failed":
            LOG.info(f"{selected_website} Update failed {EMOJIS[4]}")
            messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"{selected_website} Update failed {EMOJIS[4]}\n Please Debug {EMOJIS[10]}")

    else:
        LOG.debug(f"{mode} Update Canceled")


def auto_update(SRC_DIRECTORY, ALL_WEBSITES, SETTINGS, CONN, SELECTOR, LOG):
    """Update all enabled websites.

    Args:
        SRC_DIRECTORY (str): path to the src directory
        ALL_WEBSITES (list): list of available websites
        SETTINGS (Any): .json configuration file
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
        LOG (Any): the logger
    """

    i = 0
    mode = "Auto"
    message = "all websites"
    updates_succeeded = 0
    updates_failed = 0
    updates_skipped = 0

    if confirm_update(mode, message, SETTINGS, ALL_WEBSITES):
        os.system("clear")
        LOG.info(f"Searching for Updates {EMOJIS[8]}..")

        for website in ALL_WEBSITES:

            start_time = time.time()
            i, status = check_and_update(website, SETTINGS, i, LOG)
            i += i
            end_time = time.time()
            elapsed_time = end_time - start_time
            if status == "success":
                LOG.info(f"{website} is Up-to-date {EMOJIS[3]} | lasted: {elapsed_time:.2f} s")
                w_average_time(website, round(elapsed_time, 2), SETTINGS)
                updates_succeeded += 1
            elif status == "skipped":
                LOG.info(f"{website} Update skipped {EMOJIS[12]}")
                updates_skipped += 1
            elif status == "failed":
                LOG.info(f"{website} Update failed {EMOJIS[4]}")
                updates_failed += 1

        if i != 0:
            result = Manage_migration(SRC_DIRECTORY, CONN, SELECTOR, LOG)
            if result == "success":
                LOG.info(f"Migration completed {EMOJIS[3]}.")
                messagebox.showinfo(f"Update info [{EMOJIS[13]}]", f"""
                                    Migration completed {EMOJIS[3]}

                                    succeeded : {updates_succeeded}/{len(ALL_WEBSITES)} {EMOJIS[3]}
                                    failed : {updates_failed} {EMOJIS[4]}
                                    skipped : {updates_skipped} {EMOJIS[12]}

                                    \n\nExplore the changelogs {EMOJIS[16]}""")
            elif result == "failed":
                LOG.info(f"Migration failed {EMOJIS[4]}.")
                messagebox.showinfo(f"Migration Info {EMOJIS[13]}", f"Migration failed {EMOJIS[4]}\n Please Debug {EMOJIS[10]}")
        else:
            messagebox.showinfo(f"Update Info {EMOJIS[13]}", f"All Updates failed {EMOJIS[4]}, Please check your settings.")

    else:
        LOG.debug(f"{mode} Update Canceled")
