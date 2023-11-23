import pandas as pd
import yaml
from .utils import Delete_table


def Manage_migration(MAIN_DIRECTORY, CONN, SELECTOR, WEBSITES, LOG):
    """Migrate the CSV and YAML data to the database.

    Args:
        MAIN_DIRECTORY (str): chemin d'accès au dossier PandaScan
        CONN (Any): connexion à la DB
        SELECTOR (Any): curseur de la DB
        WEBSITES (list): liste de sites disponibles
        LOG (Any): logger d'affichage
    """

    LOG.info("Initialisation de la Migration ..")
    websites = [{'NomSite': WEBSITES[0]},
                {'NomSite': WEBSITES[1]},
                {'NomSite': WEBSITES[2]},
                {'NomSite': WEBSITES[3]}
                ]

    tables = ["Mangas", "Chapitres"]

    df_sites = pd.DataFrame(websites)
    df_sites.to_sql('SitesWeb', CONN, if_exists='replace', index=False)

    # Charger le fichier CSV [chapters_links.csv] dans un DataFrame pandas ( uniquement pour le site anime-sama )
    df_chapters_links = pd.read_csv(f'{MAIN_DIRECTORY}/update/websites/animesama/datas/chapters_links.csv')
    df_chapters_links.to_sql('ChapterLink', CONN, if_exists='replace', index=False)

    LOG.info("Vérifications et Nettoyage de la DB ..")

    for table in tables:
        Delete_table(table, CONN, SELECTOR)

    for website in websites:

        # Charger le fichier CSV [mangas.csv] dans un DataFrame pandas
        website = website['NomSite']
        df_mangas = pd.read_csv(f'{MAIN_DIRECTORY}/update/websites/{website}/datas/mangas.csv')
        df_mangas = df_mangas.rename(columns={'name': 'NomManga'})
        # Créer une nouvelle colonne "NomSite" contenant le nom du site
        df_mangas['NomSite'] = website

        # Insérer les données du DataFrame dans la table "Mangas"
        df_mangas.to_sql('Mangas', CONN, if_exists='append', index=False)

        # Charger le fichier YAML dans un dictionnaire
        with open(f'{MAIN_DIRECTORY}/update/websites/{website}/datas/mangas_chapters.yml', 'r') as fichier_yaml:
            contenu_yaml = yaml.load(fichier_yaml, Loader=yaml.FullLoader)

        # Parcourir le dictionnaire YAML et insérer les données dans la table "Chapitres"
        for manga, chapitres in contenu_yaml.items():
            for chapitre in chapitres:
                data = {'NomSite': website, 'NomManga': manga, 'Chapitres': chapitre}
                df_chapitre = pd.DataFrame([data])
                df_chapitre.to_sql('Chapitres', CONN, if_exists='append', index=False)

        # Enregistrer les modifications dans la base de données
        CONN.commit()
        LOG.info(f"{website} migrated ✅")

    LOG.info("Migration completed ✅.")
