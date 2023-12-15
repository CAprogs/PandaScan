from ..scantrad import scrap_titles, scrap_chapters


def Update_scantrad(DRIVER, PATH_TO_SCANTRAD, LOG):
    """Update scantrad datas.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_SCANTRAD (str): path to scantrad directory (update)
        LOG (Any): the logger
    """

    result = scrap_titles.Scrap_titles(DRIVER, PATH_TO_SCANTRAD, LOG)
    if result == "success":
        scrap_chapters.Scrap_chapters(DRIVER, PATH_TO_SCANTRAD, LOG)
        return 1
    else:
        return 0
