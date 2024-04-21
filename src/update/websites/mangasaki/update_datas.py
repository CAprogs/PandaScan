from ..mangasaki import scrap_titles, scrap_chapters


def Update_mangasaki(DRIVER, PATH_TO_MANGASAKI: str, LOG):
    """Update mangasaki datas.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_MANGASAKI (str): path to mangasaki directory (update)
        LOG (Any): the logger

    Returns:
        int: 1 if success , 0 if an error occured
    """

    result = scrap_titles.Scrap_titles(DRIVER, PATH_TO_MANGASAKI, LOG)
    if result == "success":
        result = scrap_chapters.Scrap_chapters(DRIVER, PATH_TO_MANGASAKI, LOG)
        if result == "success":
            return 1
        else:
            return 0
    else:
        return 0
