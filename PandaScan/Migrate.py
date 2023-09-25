import pandas as pd
import sqlite3
import yaml
import os
from pathlib import Path
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

print("Connexion à la BDD .. \n")
# Établir une connexion à la base de données SQLite
conn = sqlite3.connect(f'{script_directory}/websites/Pan_datas.db')
cursor = conn.cursor()

# ------------ Functions -------------------

def Delete_table(table):
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

def DB_print_chapters(nom_manga,nom_site):
    """Print the chapters of a manga.

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

# -------------------------------------------

# ------------------------ Migration des données CSV et YAML ------------------------------

def Migrate_datas():
    """Migrate the CSV and YAML data to the database.
    """    
    sites_data = [
        {'NomSite': 'fmteam.fr'},
        {'NomSite': 'lelscans.net'},
        {'NomSite': 'scantrad-vf'}
        ]

    tables = ["Mangas",
            "Chapitres"]
    
    df_sites = pd.DataFrame(sites_data)
    df_sites.to_sql('SitesWeb', conn, if_exists='replace', index=False)

    print("Vérifications et Nettoyage .. \n")
    for table in tables:
        Delete_table(table)

    print("Début de la Migration ..\n")

    i = 1
    for websites in sites_data:
        
        # Charger le fichier CSV dans un DataFrame pandas
        websites = websites['NomSite']
        df_mangas = pd.read_csv(f'{script_directory}/websites/{websites}/datas/mangas.csv')
        df_mangas = df_mangas.rename(columns={'name': 'NomManga'})
        # Créer une nouvelle colonne "NomSite" contenant la valeur du nom du site
        df_mangas['NomSite'] = websites

        # Charger le fichier YAML dans un dictionnaire Python
        with open(f'{script_directory}/websites/{websites}/datas/mangas_chapters.yml', 'r') as fichier_yaml:
            contenu_yaml = yaml.load(fichier_yaml, Loader=yaml.FullLoader)

        # Utiliser la méthode to_sql() pour insérer les données depuis le DataFrame dans la table Mangas
        df_mangas.to_sql('Mangas', conn, if_exists='append', index=False)

        # Parcourir le dictionnaire YAML et insérer les données dans la table Chapitres
        for manga, chapitres in contenu_yaml.items():
            for chapitre in chapitres:
                data = {'NomSite': websites, 'NomManga': manga, 'Chapitres': chapitre}
                df_chapitre = pd.DataFrame([data])
                df_chapitre.to_sql('Chapitres', conn, if_exists='append', index=False)

        # Enregistrer les modifications dans la base de données
        conn.commit()
        print(f"Migration {i} terminée ..\n")
        i += 1

    print("Fin de la Migration.")
    # Arrêter la connexion
    conn.close()


# Uncomment to test ( Print the chapters of a manga )
'''
print('\nLes chapitres disponibles pour \"blue-lock\" sont : \n')
# Afficher les chapitres d'un manga spécifique
DB_print_chapters("blue-lock","scantrad-vf")
conn.close()
'''

# Uncomment to Debug ( Migrate the CSV and YAML data to the database )
'''
Migrate_datas()
'''
