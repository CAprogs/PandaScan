from ..animesama import scrap_titles, scrap_chapters


def Update_animesama(PATH_TO_ANIMESAMA, LOG):
    """Update animesama datas.

    Args:
        PATH_TO_ANIMESAMA (str): path to animesama directory (update)
        LOG (Any): the logger
    """

    scrap_titles.Scrap_titles(PATH_TO_ANIMESAMA, LOG)
    scrap_chapters.Scrap_chapters(PATH_TO_ANIMESAMA, LOG)
