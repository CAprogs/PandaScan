from ..tcbscans import scrap_titles, scrap_chapters


def Update_tcbscans(PATH_TO_TCBSCANS: str, LOG):
    """Update tcbscans datas.

    Args:
        PATH_TO_TCBSCANS (str): path to tcbscans directory (update)
        LOG (Any): the logger

    Returns:
        int: 1 if success , 0 if an error occured
    """

    result = scrap_titles.Scrap_titles(PATH_TO_TCBSCANS, LOG)
    if result == "success":
        result = scrap_chapters.Scrap_chapters(PATH_TO_TCBSCANS, LOG)
        if result == "success":
            return 1
        else:
            return 0
    else:
        return 0
