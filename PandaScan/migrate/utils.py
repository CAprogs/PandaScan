
def Delete_table(table, CONN, SELECTOR):
    """Delete the content of a table.

    Args:
        table (str): name of the table to delete
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor
    """
    SELECTOR.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
    table_exists = SELECTOR.fetchone() is not None

    if table_exists:
        delete_query = f'DELETE FROM {table}'
        CONN.execute(delete_query)
