from ..lelmanga import scrap_titles, scrap_chapters


def update_lelmanga(PATH_TO_LELMANGA: str, LOG):
    """Update lelmanga datas.

    Args:
        PATH_TO_LELMANGA (str): path to lelmanga directory (update)
        LOG (Any): the logger

    Returns:
        int: 1 if success , 0 if an error occurred
    """
    result = scrap_titles.scrap_titles(PATH_TO_LELMANGA, LOG)
    if result == "success":
        result = scrap_chapters.scrap_chapters(PATH_TO_LELMANGA, LOG)
        if result == "success":
            return 1
        else:
            return 0
    else:
        return 0
