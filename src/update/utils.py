from tkinter import messagebox
from src.changelog.manage import generate_changelog
from src.foundation.core.essentials import DRIVER
from src.foundation.core.essentials import PATH_TO_FMTEAM
from src.foundation.core.essentials import PATH_TO_LELSCANS
from src.foundation.core.essentials import PATH_TO_SCANTRAD
from src.foundation.core.essentials import PATH_TO_ANIMESAMA
from src.foundation.core.emojis import EMOJIS


def confirm_update(mode, message):
    """Update check.

    Args:
        mode (str): "Manual" or "Auto"
        message (str): message to display

    Returns:
        bool: True(validate), False(otherwise)
    """

    result = messagebox.askquestion(f"Confirmation Check : {mode}-Update", f"Update {message} ?")
    if result == "yes":
        return True
    return False


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

    website_status = SETTINGS["websites"][selected_website]["enabled"]

    if website_status:
        from update.websites.scantrad.update_datas import Update_scantrad
        from update.websites.lelscans.update_datas import Update_lelscans
        from update.websites.fmteam.update_datas import Update_fmteam
        from update.websites.animesama.update_datas import Update_animesama

        LOG.info(f"Updating {selected_website} {EMOJIS[8]}..")

        if selected_website == "scantrad":
            Update_scantrad(DRIVER, PATH_TO_SCANTRAD, LOG)
            generate_changelog(PATH_TO_SCANTRAD, selected_website)
        elif selected_website == "lelscans":
            Update_lelscans(PATH_TO_LELSCANS, LOG)
            generate_changelog(PATH_TO_LELSCANS, selected_website)
        elif selected_website == "fmteam":
            Update_fmteam(DRIVER, PATH_TO_FMTEAM, LOG)
            generate_changelog(PATH_TO_FMTEAM, selected_website)
        elif selected_website == "animesama":
            Update_animesama(PATH_TO_ANIMESAMA, LOG)
            generate_changelog(PATH_TO_ANIMESAMA, selected_website)

        i += 1
        return i, website_status

    else:
        LOG.info(f"{selected_website} can't be updated {EMOJIS[4]} due to settings.")
        return i, website_status
