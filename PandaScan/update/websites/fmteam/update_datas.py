from ..fmteam import scrap_titles, scrap_chapters


def Update_fmteam(DRIVER, PATH_TO_FMTEAM, LOG):
    """Update fmteam datas.

    Args:
        DRIVER (Any): the chromedriver
        PATH_TO_FMTEAM (str): path to fmteam directory (update)
        LOG (Any): the logger
    """

    scrap_titles.Scrap_titles(DRIVER, PATH_TO_FMTEAM, LOG)
    scrap_chapters.Scrap_chapters(DRIVER, PATH_TO_FMTEAM, LOG)
