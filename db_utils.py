import sqlite3
import os
import time
import pandas as pd
from connector_factory import ConnectorFactory


class DbUtils:
    def __init__(self):
        pass

    @staticmethod
    def check_table_exists(table_name):
        res = DbUtils.run_query(f"SELECT name FROM sqlite_master WHERE name='{table_name}'", get_df=False)
        if res:
            exists = True
        else:
            exists = False
        return exists
    
    @staticmethod
    def run_query(query, get_df=True, verbose=True):
        if verbose:
            print("\n\nQUERY:")
            print(query)
        tic = time.perf_counter()
        con = ConnectorFactory.get_connector()
        if get_df:
            res = pd.read_sql(sql=query, con=con)
        else:
            cur = con.cursor()
            sqlite_res = cur.execute(query)
            res = [x for x in sqlite_res.fetchall()]
        con.commit()
        con.close()
        toc = time.perf_counter()
        if verbose:
            print(f"\nQuery run in {toc - tic:0.4f} seconds")
        return res
    
    @staticmethod
    def df_to_table(df, table_name, if_exists, index):
        con = ConnectorFactory.get_connector()
        res = df.to_sql(table_name,con,if_exists=if_exists,index=index)
        con.commit()
        con.close()
        return res
    
    @staticmethod
    def reset_table(table_name, cols):
        DbUtils.run_query(f"DROP TABLE IF EXISTS {table_name}", get_df=False)
        col_start = cols[0] + " PRIMARY KEY, "
        non_pk_cols = cols[1:]
        col_end = ", ".join(non_pk_cols)
        col_str = col_start + col_end
        DbUtils.run_query(f"CREATE TABLE {table_name}({col_str})", get_df=False)

    @staticmethod
    def get_column_names(table_name, verbose=True):
        res = DbUtils.run_query(f"PRAGMA table_info({table_name})", get_df=False, verbose=verbose)
        column_names = []
        for row in res:
            column_names.append(row[1])
        return column_names
    
    @staticmethod
    def get_table_names(verbose=True):
        res = DbUtils.run_query("""
        SELECT 
            name
        FROM 
            sqlite_schema
        WHERE 
            type ='table' AND 
            name NOT LIKE 'sqlite_%'
        """, get_df=False, verbose=verbose)
        table_names = []
        for row in res:
            table_names.append(row[0])
        return table_names
