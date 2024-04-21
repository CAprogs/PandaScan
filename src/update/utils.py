import json
from tkinter import messagebox
from src.changelog.manage import generate_changelog
from src.foundation.core.essentials import DRIVER, PATH_TO_CONFIG
from src.foundation.core.essentials import PATH_TO_FMTEAM, PATH_TO_LELSCANS
from src.foundation.core.essentials import PATH_TO_ANIMESAMA, PATH_TO_TCBSCANS, PATH_TO_LELMANGA
from src.foundation.core.essentials import PATH_TO_MANGANELO, PATH_TO_MANGAMOINS, PATH_TO_MANGASAKI
from src.foundation.core.essentials import PATH_TO_LHTRANSLATION
from src.foundation.core.emojis import EMOJIS


def get_average_time(mode, selected_website, SETTINGS, ALL_WEBSITES=None):
    """Get the average time of an update.

    Args:
        mode (str): "Manual" or "Auto"
        selected_website (str): name of the website to update
        SETTINGS (Any): .json configuration file
        ALL_WEBSITES (list/optional): list of available websites

    Returns:
        str: average time of an update
    """

    average_time = ""
    if mode.lower() == "manual" and SETTINGS["websites"][selected_website]["time_to_update"] != 0:
        update_time = SETTINGS["websites"][selected_website]["time_to_update"]
        if update_time > 3600:
            average_time = f"Average duration : {update_time / 3600:.2f} h"
        elif update_time > 60:
            average_time = f"Average duration : {update_time / 60:.2f} min"
        else:
            average_time = f"Average duration : {update_time} s"
    elif mode.lower() == "auto":
        total_time = 0
        for website in [website for website in ALL_WEBSITES if SETTINGS["websites"][website]["enabled"]]:
            if SETTINGS["websites"][website]["time_to_update"] != 0:
                total_time += SETTINGS["websites"][website]["time_to_update"]
        if total_time != 0:
            if total_time > 3600:
                total_time = f"{total_time / 3600:.2f} h"
            elif total_time > 60:
                total_time = f"{total_time / 60:.2f} min"
            else:
                total_time = f"{total_time} s"
            average_time = f"Average duration : {total_time}"
    return average_time


def confirm_update(mode, message, SETTINGS, ALL_WEBSITES=None):
    """Ask for confirmation before updating.

    Args:
        mode (str): "Manual" or "Auto"
        message (str): message to display
        SETTINGS (Any): .json configuration file
        ALL_WEBSITES (list/optional): list of available websites

    Returns:
        bool: True(validate), False(otherwise)
    """

    average_time = get_average_time(mode, message, SETTINGS, ALL_WEBSITES)
    result = messagebox.askquestion(f"Confirmation Check : {mode}-Update", f"Update {message} ?\n\n{average_time}")
    if result == "yes":
        return True
    return False


def w_average_time(website, elapsed_time, SETTINGS):
    """Write the average time of an update.

    Args:
        website (str): name of the website updated
        SETTINGS (Any): .json configuration file
        elapsed_time (float): time taken by an update
    """

    SETTINGS["websites"][website]["time_to_update"] = elapsed_time
    with open(PATH_TO_CONFIG, "w") as f:
        json.dump(SETTINGS, f, indent=4)


def check_and_update(selected_website, SETTINGS, i, LOG):
    """Check if a website can be updated and perform the update.

    Args:
        selected_website (str): name of the website to update
        SETTINGS (Any): .json configuration file
        i (int): counter
        LOG (Any): the logger

    Returns:
        int: +1 (if updated), +0 (otherwise)
        bool: True(website's update is enabled), False(otherwise)
    """

    if SETTINGS["websites"][selected_website]["enabled"]:
        from src.update.websites.lelscans.update_datas import Update_lelscans
        from src.update.websites.fmteam.update_datas import Update_fmteam
        from src.update.websites.animesama.update_datas import Update_animesama
        from src.update.websites.tcbscans.update_datas import Update_tcbscans
        from src.update.websites.lelmanga.update_datas import Update_lelmanga
        from src.update.websites.manganelo.update_datas import Update_manganelo
        from src.update.websites.mangamoins.update_datas import Update_mangamoins
        from src.update.websites.mangasaki.update_datas import Update_mangasaki
        from src.update.websites.lhtranslation.update_datas import Update_lhtranslation

        LOG.info(f"Updating {selected_website} {EMOJIS[8]}")

        if selected_website == "lelscans":
            path = PATH_TO_LELSCANS
            i = Update_lelscans(path, LOG)
        elif selected_website == "fmteam":
            path = PATH_TO_FMTEAM
            i = Update_fmteam(DRIVER, path, LOG)
        elif selected_website == "animesama":
            path = PATH_TO_ANIMESAMA
            i = Update_animesama(path, LOG)
        elif selected_website == "tcbscans":
            path = PATH_TO_TCBSCANS
            i = Update_tcbscans(path, LOG)
        elif selected_website == "lelmanga":
            path = PATH_TO_LELMANGA
            i = Update_lelmanga(path, LOG)
        elif selected_website == "manganelo":
            path = PATH_TO_MANGANELO
            i = Update_manganelo(path, LOG)
        elif selected_website == "mangamoins":
            path = PATH_TO_MANGAMOINS
            i = Update_mangamoins(path, LOG)
        elif selected_website == "mangasaki":
            path = PATH_TO_MANGASAKI
            i = Update_mangasaki(DRIVER, path, LOG)
        elif selected_website == "lhtranslation":
            path = PATH_TO_LHTRANSLATION
            i = Update_lhtranslation(DRIVER, path, LOG)
        else:
            LOG.info(f"{selected_website} isn't supported {EMOJIS[4]}.")
            status = "failed"

        if i != 0:
            status = generate_changelog(path, selected_website)
        else:
            status = "failed"
    else:
        status = "skipped"

    return i, status
