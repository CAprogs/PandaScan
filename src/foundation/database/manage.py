import sqlite3 as sql
from tkinter import messagebox
from .utils import create_db_from_ddl
from ..core.emojis import EMOJIS
from ..selenium.utils import exit_app
# from datetime import datetime


TABLES = ['Websites', 'Mangas', 'Chapters', 'Historic', 'Duplicates']


class DatabaseHandler:
    def __init__(self, path_to_db: str, path_to_ddl: str):
        try:
            create_db_from_ddl(path_to_db, path_to_ddl, overwrite=False)
            self.conn = sql.connect(path_to_db)
            self.cursor = self.conn.cursor()
            print(f"\nDatas Loaded {EMOJIS[3]}")
        except sql.Error as e:
            messagebox.showinfo(f"An Error occured when trying to load Datas [{EMOJIS[15]}] : {e}")
            exit_app()

    def insert_data(self, table_name: str, data: dict):
        # Insert data into a table
        placeholders = ', '.join(['?' for _ in data])
        query = f'''
            INSERT INTO {table_name} ({', '.join(data.keys())})
            VALUES ({placeholders})
        '''
        self.cursor.execute(query, tuple(data.values()))
        self.conn.commit()
        if self.cursor.rowcount != 0:
            # print(f"Inserted {self.cursor.rowcount} rows into {table_name} 📥")
            return True
        else:
            # print(f"No rows inserted into {table_name} !")
            return False

    def remove_data(self, table_name: str, condition: str = None):
        # Remove data from a table based on a condition or not
        query = f'''
            DELETE FROM {table_name}
        '''
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()
        if self.cursor.rowcount != 0:
            # print(f"Deleted {self.cursor.rowcount} rows from {table_name} 🧹")
            return True
        else:
            # print(f"No rows deleted from {table_name} !")
            return False

    def update_data(self, table_name: str, data: str, condition: str = None):
        # Update data in the table based on a condition or not
        query = f'''
            UPDATE {table_name}
            SET {data}
        '''
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        self.conn.commit()
        if self.cursor.rowcount != 0:
            # print(f"Updated {self.cursor.rowcount} rows from {table_name} 🔄")
            return True
        else:
            # print(f"No rows updated from {table_name} !")
            return False

    def query_data(self, table_name: str, columns: list, condition: str = None):
        # Query data from a table
        columns_str = ', '.join(columns)
        query = f'''
            SELECT {columns_str}
            FROM {table_name}
        '''
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        all_results = self.cursor.fetchall()
        if result is None:
            # print(f"\n\nNo rows found in {table_name} !")
            return None
        elif len(columns) == 1 and columns[0] != '*':
            return result
        else:
            return all_results

    def insert_historic(self, table_name: str, data: dict):
        # insert data into the historic table
        pass
