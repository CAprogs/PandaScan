from ..lelscans import scrap_titles, scrap_chapters


def update_lelscans(PATH_TO_LELSCANS: str, LOG):
    """Update lelscans datas.

    Args:
        PATH_TO_LELSCANS (str): path to lelscans directory (update)
        LOG (Any): the logger

    Returns:
        int: 1 if success , 0 if an error occurred
    """
    result = scrap_titles.scrap_titles(PATH_TO_LELSCANS, LOG)
    if result == "success":
        result = scrap_chapters.scrap_chapters(PATH_TO_LELSCANS, LOG)
        if result == "success":
            return 1
        else:
            return 0
    else:
        return 0
