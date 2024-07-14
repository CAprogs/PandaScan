
def clean_table(table: str, CONN, SELECTOR):
    """Empty the content of a table.

    Args:
        table (str): name of the table to delete
        CONN (Any): DB connection
        SELECTOR (Any): DB cursor

    Returns:
        bool: True if the table exists, False otherwise
    """
    SELECTOR.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
    table_exists = SELECTOR.fetchone() is not None

    if table_exists:
        delete_query = f'DELETE FROM {table}'
        CONN.execute(delete_query)
        return True
    else:
        return False


def found_and_clean_duplicates(df, columns: list):
    """
    Search duplicated values from a CSV based on a combination of columns

    Args:
        df (DataFrame): dataframe to treat
        columns (list): list of columns used to find duplicates

    Returns:
        tuple: If the dataframe doesn't contains any duplicates then return (df, None) otherwise (df, df_duplicates).
    """
    df_duplicates = df[df.duplicated(subset=columns, keep=False)]

    if not df_duplicates.empty:
        df.drop_duplicates(subset=columns, inplace=True)
        return df, df_duplicates
    return df, None
