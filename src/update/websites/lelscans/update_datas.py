from ..lelscans import scrap_titles, scrap_chapters


def Update_lelscans(PATH_TO_LELSCANS, LOG):
    """Update lelscans datas.

    Args:
        PATH_TO_LELSCANS (str): path to lelscans directory (update)
        LOG (Any): the logger

    Returns:
        int: 1 if success , 0 if an error occurred
    """

    result = scrap_titles.Scrap_titles(PATH_TO_LELSCANS, LOG)
    if result == "success":
        result = scrap_chapters.Scrap_chapters(PATH_TO_LELSCANS, LOG)
        if result == "success":
            return 1
        else:
            return 0
    else:
        return 0
