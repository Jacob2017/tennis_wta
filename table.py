import sqlite3
import os
# from sqlite_connector import SQLiteConnector

class Table:

    def __init__(self):
        pass
    
    @staticmethod
    def create_table(db_name, db_path, table_name, columns):
        db_full_path = os.path.join(db_path,db_name)
        con = sqlite3.connect(db_full_path)
        cur = con.cursor()

        column_str = ", ".join(columns)

        success = False

        try:
            cur.execute(f"CREATE TABLE {table_name}({column_str})")
            success = True
        except sqlite3.OperationalError as e:
            # print(e)
            if "already exists" in str(e):
                print(f"WARNING: Table {table_name} already exists.")
                success = True
            else:
                print("ERROR: Table creation unsuccessful.")
                success = False

        return success
        