def Update_lelscans():
    """Update the mangas chapters.
    """
    from Scrap_Chapters_lelscans import Scrap_Chapters
    from Scrap_Titles_lelscans import Scrap_Titles
    from Changelog_lelscans import generate_changelog

    Scrap_Titles()
    Scrap_Chapters()
    generate_changelog()