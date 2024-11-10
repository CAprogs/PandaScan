from ..manganelo import scrap_titles, scrap_chapters


def update_manganelo(PATH_TO_MANGANELO: str, LOG):
    """Update manganelo datas.

    Args:
        PATH_TO_MANGANELO (str): path to manganelo directory (update)
        LOG (Any): the logger

    Returns:
        int: 1 if success , 0 if an error occured
    """
    result = scrap_titles.scrap_titles(PATH_TO_MANGANELO, LOG)
    if result == "success":
        result = scrap_chapters.scrap_chapters(PATH_TO_MANGANELO, LOG)
        if result == "success":
            return 1
        else:
            return 0
    else:
        return 0
