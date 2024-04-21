import pandas as pd
from .utils import Delete_table
from src.foundation.core.essentials import WEBSITES_DICT
from src.foundation.core.emojis import EMOJIS


def Manage_migration(SRC_DIRECTORY: str, CONN, SELECTOR, LOG):
    """Migrate the CSV and YAML data to the database.

    Args:
        SRC_DIRECTORY (str): path to the src directory
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
        LOG (Any): the logger

    Returns:
        str: 'success' if passed, 'failed' if an error occured
    """

    LOG.info("Datas migration ..")
    websites = [{'NomSite': website} for website in WEBSITES_DICT.keys()]

    nb_websites = len(websites)
    latest_website_index = nb_websites - 1
    failed_migrations = []

    tables = ["Mangas", "Chapitres", "ChapterLink"]

    # df_sites -> Table "SitesWeb"
    df_sites = pd.DataFrame(websites)
    df_sites.to_sql('SitesWeb', CONN, if_exists='replace', index=False)

    LOG.info("Database Checks and Cleanup ..")

    for table in tables:
        result = Delete_table(table, CONN, SELECTOR)
        if result:
            LOG.info(f"Table {table} deleted ..")

    for website in websites:
        try:
            website = website['NomSite']

            # [mangas.csv] -> Table "Mangas"
            df_mangas = pd.read_csv(f'{SRC_DIRECTORY}/update/websites/{website}/datas/mangas.csv')
            df_mangas['NomSite'] = website
            df_mangas.to_sql('Mangas', CONN, if_exists='append', index=False)

            # [chapters_links.csv] -> Table "ChapterLink"
            df_chapters_links = pd.read_csv(f'{SRC_DIRECTORY}/update/websites/{website}/datas/chapters_links.csv')
            df_chapters_links.to_sql('ChapterLink', CONN, if_exists='append', index=False)

            # Save changes to the database
            CONN.commit()
            LOG.info(f"{website} migrated {EMOJIS[3]}")

        except Exception as e:
            failed_migrations.append(website)
            LOG.info(f"Error : {e} | {website} failed to migrate {EMOJIS[4]}")
            if website.index != latest_website_index:
                continue

    if len(failed_migrations) == nb_websites:
        return "failed"
    elif failed_migrations != []:
        LOG.debug(f"\n{len(failed_migrations)} mangas failed ..\n")
        for website in failed_migrations:
            LOG.debug(website)

    return "success"
