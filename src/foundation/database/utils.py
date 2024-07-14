import os
from ..core.emojis import EMOJIS


def create_db_from_ddl(path_to_db: str, path_to_ddl: str, overwrite: bool):
    """Execute a SQL script to create a database.

    Args:
        path_to_db (str): path to the database file to overwrite or create.
        path_to_ddl (str): path to the SQL file to execute.
        overwrite (bool): if True, overwrite the existant db file otherwise do nothing.
    """
    if not os.path.exists(path_to_ddl):
        raise OSError(f"The DDL script file was not found at path: {path_to_ddl}")
    if not os.path.exists(path_to_db) or overwrite:
        with open(path_to_db, 'w') as f:
            f.write('')
        db_name = os.path.basename(path_to_db).replace('.db', '')
        os.system(f"sqlite3 {path_to_db} < {path_to_ddl}")
        print(f"\nDatabase '{db_name}' successfully created {EMOJIS[3]}")
