from tkinter import messagebox
from changelog.manage import generate_changelog
from foundation.core.essentials import DRIVER
from foundation.core.essentials import PATH_TO_FMTEAM
from foundation.core.essentials import PATH_TO_LELSCANS
from foundation.core.essentials import PATH_TO_SCANTRAD
from foundation.core.essentials import PATH_TO_ANIMESAMA


def confirm_update(mode):
    """Update check.

    Args:
        mode (str): mode de mise à jour

    Returns:
        bool: True = validée, False = refusée
    """

    result = messagebox.askquestion(f"Confirmation Check : {mode}", f"Proceed {mode}-Update ❓")
    if result == "yes":
        return True
    return False


def check_and_update(selected_website, SETTINGS, i, LOG):
    """Check if a website can be updated and perform the update.

    Args:
        selected_website (str): site à mettre à jour
        SETTINGS (Any): fichier de configuration json
        i (int): variable de suivi de mis à jour
        LOG (Any): logger d'affichage

    Returns:
        int: i (+1 si mis à jour, +0 sinon)
    """
    if SETTINGS["websites"][selected_website]["enabled"]:
        from update.websites.scantrad.update_datas import Update_scantrad
        from update.websites.lelscans.update_datas import Update_lelscans
        from update.websites.fmteam.update_datas import Update_fmteam
        from update.websites.animesama.update_datas import Update_animesama

        LOG.info(f"Updating {selected_website} 🔄..")

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
        LOG.info(f"{selected_website} is Up-to-date ✅")
        return i

    else:
        LOG.info(f"'{selected_website}' can't be updated due to settings.")
        return i
