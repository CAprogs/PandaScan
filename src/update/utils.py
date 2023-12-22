import json
from tkinter import messagebox
from src.changelog.manage import generate_changelog
from src.foundation.core.essentials import DRIVER, PATH_TO_CONFIG
from src.foundation.core.essentials import PATH_TO_FMTEAM
from src.foundation.core.essentials import PATH_TO_LELSCANS
from src.foundation.core.essentials import PATH_TO_SCANTRAD
from src.foundation.core.essentials import PATH_TO_ANIMESAMA
from src.foundation.core.essentials import PATH_TO_TCBSCANS
from src.foundation.core.essentials import PATH_TO_LELMANGA
from src.foundation.core.essentials import PATH_TO_MANGANELO
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
        average_time = f"Average duration : {SETTINGS["websites"][selected_website]["time_to_update"]} s"
    elif mode.lower() == "auto":
        total_time = 0
        for website in [website for website in ALL_WEBSITES if SETTINGS["websites"][website]["enabled"]]:
            if SETTINGS["websites"][website]["time_to_update"] != 0:
                total_time += SETTINGS["websites"][website]["time_to_update"]
        if total_time != 0:
            average_time = f"Average duration : {total_time} s"
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
        from src.update.websites.scantrad.update_datas import Update_scantrad
        from src.update.websites.lelscans.update_datas import Update_lelscans
        from src.update.websites.fmteam.update_datas import Update_fmteam
        from src.update.websites.animesama.update_datas import Update_animesama
        from src.update.websites.tcbscans.update_datas import Update_tcbscans
        from src.update.websites.lelmanga.update_datas import Update_lelmanga
        from src.update.websites.manganelo.update_datas import Update_manganelo

        LOG.info(f"Updating {selected_website} {EMOJIS[8]}")

        if selected_website == "scantrad":
            i = Update_scantrad(DRIVER, PATH_TO_SCANTRAD, LOG)
            if i != 0:
                status = generate_changelog(PATH_TO_SCANTRAD, selected_website)
        elif selected_website == "lelscans":
            i = Update_lelscans(PATH_TO_LELSCANS, LOG)
            if i != 0:
                status = generate_changelog(PATH_TO_LELSCANS, selected_website)
        elif selected_website == "fmteam":
            i = Update_fmteam(DRIVER, PATH_TO_FMTEAM, LOG)
            if i != 0:
                status = generate_changelog(PATH_TO_FMTEAM, selected_website)
        elif selected_website == "animesama":
            i = Update_animesama(PATH_TO_ANIMESAMA, LOG)
            if i != 0:
                status = generate_changelog(PATH_TO_ANIMESAMA, selected_website)
        elif selected_website == "tcbscans":
            i = Update_tcbscans(PATH_TO_TCBSCANS, LOG)
            if i != 0:
                status = generate_changelog(PATH_TO_TCBSCANS, selected_website)
        elif selected_website == "lelmanga":
            i = Update_lelmanga(PATH_TO_LELMANGA, LOG)
            if i != 0:
                status = generate_changelog(PATH_TO_LELMANGA, selected_website)
        elif selected_website == "manganelo":
            i = Update_manganelo(PATH_TO_MANGANELO, LOG)
            if i != 0:
                status = generate_changelog(PATH_TO_MANGANELO, selected_website)
        else:
            LOG.info(f"{selected_website} isn't supported {EMOJIS[4]}.")
            status = "failed"

    else:
        status = "skipped"
    
    return i, status
