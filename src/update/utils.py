from tkinter import messagebox
from src.changelog.manage import generate_changelog
from src.foundation.core.essentials import DRIVER
from src.foundation.core.essentials import PATH_TO_FMTEAM
from src.foundation.core.essentials import PATH_TO_LELSCANS
from src.foundation.core.essentials import PATH_TO_SCANTRAD
from src.foundation.core.essentials import PATH_TO_ANIMESAMA
from src.foundation.core.essentials import PATH_TO_TCBSCANS
from src.foundation.core.essentials import PATH_TO_LELMANGA
from src.foundation.core.essentials import PATH_TO_MANGANELO
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
        from src.update.websites.scantrad.update_datas import Update_scantrad
        from src.update.websites.lelscans.update_datas import Update_lelscans
        from src.update.websites.fmteam.update_datas import Update_fmteam
        from src.update.websites.animesama.update_datas import Update_animesama
        from src.update.websites.tcbscans.update_datas import Update_tcbscans
        from src.update.websites.lelmanga.update_datas import Update_lelmanga
        from src.update.websites.manganelo.update_datas import Update_manganelo

        LOG.info(f"Updating {selected_website} {EMOJIS[8]}..")

        if selected_website == "scantrad":
            i = Update_scantrad(DRIVER, PATH_TO_SCANTRAD, LOG)
            if i != 0:
                generate_changelog(PATH_TO_SCANTRAD, selected_website)
        elif selected_website == "lelscans":
            i = Update_lelscans(PATH_TO_LELSCANS, LOG)
            if i != 0:
                generate_changelog(PATH_TO_LELSCANS, selected_website)
        elif selected_website == "fmteam":
            i = Update_fmteam(DRIVER, PATH_TO_FMTEAM, LOG)
            if i != 0:
                generate_changelog(PATH_TO_FMTEAM, selected_website)
        elif selected_website == "animesama":
            i = Update_animesama(PATH_TO_ANIMESAMA, LOG)
            if i != 0:
                generate_changelog(PATH_TO_ANIMESAMA, selected_website)
        elif selected_website == "tcbscans":
            i = Update_tcbscans(PATH_TO_TCBSCANS, LOG)
            if i != 0:
                generate_changelog(PATH_TO_TCBSCANS, selected_website)
        elif selected_website == "lelmanga":
            i = Update_lelmanga(PATH_TO_LELMANGA, LOG)
            if i != 0:
                generate_changelog(PATH_TO_LELMANGA, selected_website)
        elif selected_website == "manganelo":
            i = Update_manganelo(PATH_TO_MANGANELO, LOG)
            if i != 0:
                generate_changelog(PATH_TO_MANGANELO, selected_website)
        else:
            LOG.info(f"{selected_website} isn't supported {EMOJIS[4]}.")
            return i, website_status

        return i, website_status

    else:
        LOG.info(f"{selected_website} can't be updated {EMOJIS[4]} due to settings.")
        return i, website_status
