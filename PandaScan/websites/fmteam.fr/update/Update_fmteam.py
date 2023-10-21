def Update_fmteam():
    """Update the mangas chapters.
    """
    from Scrap_Chapters_fmteam import Scrap_Chapters
    from Scrap_Titles_fmteam import Scrap_Titles
    from Changelog_fmteam import generate_changelog
        
    Scrap_Titles()
    Scrap_Chapters()
    generate_changelog()