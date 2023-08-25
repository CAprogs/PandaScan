from Scrap_Chapters_scantrad import Scrap_Chapters
from Scrap_Titles_scantrad import Scrap_Titles
from Changelog_scantrad import generate_changelog

def Update_scantrad():
    Scrap_Titles()
    Scrap_Chapters()
    generate_changelog()