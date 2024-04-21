from ..mangamoins import scrap_titles, scrap_chapters


def Update_mangamoins(PATH_TO_MANGAMOINS: str, LOG):
    """Update mangamoins datas.

    Args:
        PATH_TO_MANGAMOINS (str): path to mangamoins directory (update)
        LOG (Any): the logger

    Returns:
        int: 1 if success , 0 if an error occured
    """

    result = scrap_titles.Scrap_titles(PATH_TO_MANGAMOINS, LOG)
    if result == "success":
        result = scrap_chapters.Scrap_chapters(PATH_TO_MANGAMOINS, LOG)
        if result == "success":
            return 1
        else:
            return 0
    else:
        return 0
