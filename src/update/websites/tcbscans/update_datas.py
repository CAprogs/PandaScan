from ..tcbscans import scrap_titles, scrap_chapters


def Update_tcbscans(PATH_TO_TCBSCANS, LOG):
    """Update tcbscans datas.

    Args:
        PATH_TO_TCBSCANS (str): path to tcbscans directory (update)
        LOG (Any): the logger
    """

    result = scrap_titles.Scrap_titles(PATH_TO_TCBSCANS, LOG)
    if result == "success":
        scrap_chapters.Scrap_chapters(PATH_TO_TCBSCANS, LOG)
        return 1
    else:
        return 0
