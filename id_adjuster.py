from sqlite_operator import SqliteOperator
import constants as cn

class IdAdjuster(SqliteOperator):
    def __init__(self,db_folder,db_file):
        super().__init__(db_folder,db_file)

    def adjust(self):
        IdAdjuster.reset_table("wta_players_v2",cn.output_cols)

    @staticmethod
    def reset_table(table_name, cols=cn.output_cols):
        con = SqliteOperator.get_sqlite_connector(cn.db_folder,cn.db_file)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        col_start = cols[0] + " PRIMARY KEY, "
        non_pk_cols = cols[1:]
        col_end = ", ".join(non_pk_cols)
        col_str = col_start + col_end
        cur.execute(f"CREATE TABLE {table_name}({col_str})")
        con.close()

    