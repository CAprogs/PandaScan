import pandas as pd
from .utils import clean_table, found_and_clean_duplicates
from src.foundation.core.essentials import SETTINGS
from src.foundation.core.emojis import EMOJIS
from src.foundation.database.manage import TABLES


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
    websites = []
    for key in SETTINGS["websites"].keys():
        if key != 'fav_language':
            websites.append({'Website': key,
                             'Language': SETTINGS["websites"][key]["language"],
                             'Link': SETTINGS["websites"][key]["link"],
                             'n_update': SETTINGS["websites"][key]["n_update"],
                             'n_manga': SETTINGS["websites"][key]["n_manga"],
                             'time_to_update': SETTINGS["websites"][key]["time_to_update"],
                             'last_update': SETTINGS["websites"][key]["last_update"]
                             })

    nb_websites = len(websites)
    latest_website_index = nb_websites - 1
    failed_migrations = []

    tables_to_clean = [TABLES[0], TABLES[1], TABLES[2], TABLES[4]]

    LOG.info("Database Checks and Cleanup ..")

    for table in tables_to_clean:
        result = clean_table(table, CONN, SELECTOR)
        if result:
            LOG.info(f"Table {table} emptied ..")

    # df_sites -> Table "Websites"
    df_sites = pd.DataFrame(websites)
    df_sites.to_sql(TABLES[0], CONN, if_exists='append', index=False)

    for website in websites:
        try:
            website = website['Website']

            # [mangas.csv] -> Table "Mangas"
            df_mangas = pd.read_csv(f'{SRC_DIRECTORY}/update/websites/{website}/datas/mangas.csv')
            df_mangas['Website'] = website
            df_mangas.to_sql(TABLES[1], CONN, if_exists='append', index=False)

            # [chapters_links.csv] -> Table "Chapters"
            df_chapters_links = pd.read_csv(f'{SRC_DIRECTORY}/update/websites/{website}/datas/chapters_links.csv')
            df_chapters_links, df_duplicates = found_and_clean_duplicates(df_chapters_links, ['Website', 'MangaName', 'Chapter'])
            df_chapters_links.to_sql(TABLES[2], CONN, if_exists='append', index=False)

            # [df_duplicates] -> Table "Duplicates"
            if df_duplicates is not None:
                df_duplicates.to_sql(TABLES[4], CONN, if_exists='append', index=False)

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
