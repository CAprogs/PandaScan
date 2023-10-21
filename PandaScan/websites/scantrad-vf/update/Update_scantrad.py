def Update_scantrad():
    """
    Fonction qui permet de mettre à jour les données de scantrad-vf.co
    """
    from Scrap_Chapters_scantrad import Scrap_Chapters
    from Scrap_Titles_scantrad import Scrap_Titles
    from Changelog_scantrad import generate_changelog    
    
    Scrap_Titles()
    Scrap_Chapters()
    generate_changelog()