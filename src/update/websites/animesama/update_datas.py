from ..animesama import scrap_titles, scrap_chapters


def Update_animesama(PATH_TO_ANIMESAMA, LOG):
    """Update animesama datas.

    Args:
        PATH_TO_ANIMESAMA (str): path to animesama directory (update)
        LOG (Any): the logger
    """

    result = scrap_titles.Scrap_titles(PATH_TO_ANIMESAMA, LOG)
    if result == "success":
        scrap_chapters.Scrap_chapters(PATH_TO_ANIMESAMA, LOG)
        return 1
    else:
        return 0

