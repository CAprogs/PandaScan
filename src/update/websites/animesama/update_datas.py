from ..animesama import scrap_titles, scrap_chapters


def Update_animesama(PATH_TO_ANIMESAMA, LOG):
    """Update animesama datas.

    Args:
        PATH_TO_ANIMESAMA (str): path to animesama directory (update)
        LOG (Any): the logger

    Returns:
        int: 1 if success , 0 if an error occured
    """

    result = scrap_titles.Scrap_titles(PATH_TO_ANIMESAMA, LOG)
    if result == "success":
        result = scrap_chapters.Scrap_chapters(PATH_TO_ANIMESAMA, LOG)
        if result == "success":
            return 1
        else:
            return 0
    else:
        return 0
