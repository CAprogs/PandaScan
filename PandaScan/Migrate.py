import pandas as pd
import yaml

# ========================= Functions =========================

def Delete_table(table,conn,cursor):
    """Delete the content of a table.

    Args:
        table (str): the table to delete.
    """
    # Vérifier si la table existe
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
    table_exists = cursor.fetchone() is not None

    if table_exists:
        # Si la table existe, supprimer son contenu
        delete_query = f'DELETE FROM {table}'
        conn.execute(delete_query)

def DB_print_chapters(nom_manga,nom_site,conn,cursor): # for test purpose
    """Print the chapters of a specific manga.
        
    Args:
        nom_manga (str): the manga name.
        nom_site (str): the website name.
    """    
    # requête SQL pour récupérer les chapitres du manga spécifié
    cursor.execute("SELECT Chapitres FROM Chapitres WHERE NomManga = ? AND NomSite = ?", (nom_manga,nom_site))
    chapitres = cursor.fetchall()

    # Afficher les chapitres disponibles
    for chapitre in chapitres:
        print(chapitre[0])
    conn.close()

# =========================  CSV & YAML => Sqlite DB =========================

def Migrate_datas(script_directory,conn,cursor):
    """Migrate the CSV and YAML data to the database.
    """
    print("\nInitialisation de la Migration ..\n")    
    websites = [
        {'NomSite': 'fmteam.fr'},
        {'NomSite': 'lelscans.net'},
        {'NomSite': 'scantrad-vf'}
        ]

    tables = ["Mangas",
            "Chapitres"]
    
    df_sites = pd.DataFrame(websites)
    df_sites.to_sql('SitesWeb', conn, if_exists='replace', index=False)

    print("Vérifications et Nettoyage de la DB ..\n")
    for table in tables:
        Delete_table(table,conn,cursor)

    print("Début de la Migration ..\n")

    for website in websites:
        
        # Charger le fichier CSV dans un DataFrame pandas
        website = website['NomSite']
        df_mangas = pd.read_csv(f'{script_directory}/websites/{website}/datas/mangas.csv')
        df_mangas = df_mangas.rename(columns={'name': 'NomManga'})
        # Créer une nouvelle colonne "NomSite" contenant la valeur du nom du site
        df_mangas['NomSite'] = website

        # Utiliser la méthode to_sql() pour insérer les données depuis le DataFrame dans la table Mangas
        df_mangas.to_sql('Mangas', conn, if_exists='append', index=False)

        # Charger le fichier YAML dans un dictionnaire Python
        with open(f'{script_directory}/websites/{website}/datas/mangas_chapters.yml', 'r') as fichier_yaml:
            contenu_yaml = yaml.load(fichier_yaml, Loader=yaml.FullLoader)

        # Parcourir le dictionnaire YAML et insérer les données dans la table Chapitres
        for manga, chapitres in contenu_yaml.items():
            for chapitre in chapitres:
                data = {'NomSite': website, 'NomManga': manga, 'Chapitres': chapitre}
                df_chapitre = pd.DataFrame([data])
                df_chapitre.to_sql('Chapitres', conn, if_exists='append', index=False)

        # Enregistrer les modifications dans la base de données
        conn.commit()
        print(f"{website} migrated ✅")                 ##### Track activity

    print("\nEnd of Migration.")                        ##### Track activity