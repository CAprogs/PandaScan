import pandas as pd
import yaml
from .utils import Delete_table
from src.foundation.core.emojis import EMOJIS


def Manage_migration(MAIN_DIRECTORY, CONN, SELECTOR, WEBSITES, LOG):
    """Migrate the CSV and YAML data to the database.

    Args:
        MAIN_DIRECTORY (str): path to the working directory
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
        WEBSITES (list): list of available websites
        LOG (Any): the logger
    """

    LOG.info("Datas migration ..")
    websites = [{'NomSite': WEBSITES[0]},
                {'NomSite': WEBSITES[1]},
                {'NomSite': WEBSITES[2]},
                {'NomSite': WEBSITES[3]},
                {'NomSite': WEBSITES[4]}
                ]

    tables = ["Mangas", "Chapitres"]

    df_sites = pd.DataFrame(websites)
    df_sites.to_sql('SitesWeb', CONN, if_exists='replace', index=False)

    # Charger le fichier CSV [chapters_links.csv] dans un DataFrame pandas (animesama & tcbscans)
    df_animesama = pd.read_csv(f'{MAIN_DIRECTORY}/src/update/websites/animesama/datas/chapters_links.csv')
    df_tcbscans = pd.read_csv(f'{MAIN_DIRECTORY}/src/update/websites/tcbscans/datas/chapters_links.csv')
    # Concaténer les deux DataFrames & enregistrer les données dans la table "ChapterLink"
    df_chapters_links = pd.concat([df_animesama, df_tcbscans], ignore_index=True)
    df_chapters_links.to_sql('ChapterLink', CONN, if_exists='replace', index=False)

    LOG.info("Database Checks and Cleanup ..")

    for table in tables:
        Delete_table(table, CONN, SELECTOR)

    for website in websites:

        # Charger le fichier CSV [mangas.csv] dans un DataFrame pandas
        website = website['NomSite']
        df_mangas = pd.read_csv(f'{MAIN_DIRECTORY}/src/update/websites/{website}/datas/mangas.csv')
        df_mangas['NomSite'] = website
        df_mangas.to_sql('Mangas', CONN, if_exists='append', index=False)

        # Charger le fichier YAML [mangas_chapters.yml] dans un dictionnaire
        with open(f'{MAIN_DIRECTORY}/src/update/websites/{website}/datas/mangas_chapters.yml', 'r') as file:
            yaml_content = yaml.load(file, Loader=yaml.FullLoader)

        # Parcourir le dictionnaire et insérer les données dans la table "Chapitres"
        for manga, chapitres in yaml_content.items():
            for chapitre in chapitres:
                data = {'NomSite': website, 'NomManga': manga, 'Chapitres': chapitre}
                df_chapitre = pd.DataFrame([data])
                df_chapitre.to_sql('Chapitres', CONN, if_exists='append', index=False)

        # Enregistrer les modifications dans la DB
        CONN.commit()
        LOG.info(f"{website} migrated {EMOJIS[3]}")

    LOG.info(f"Migration completed {EMOJIS[3]}.")
