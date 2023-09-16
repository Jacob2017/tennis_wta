from sqlite_operator import SqliteOperator
from utils import df_print
import constants as cn
from db_utils import DbUtils
import sys

class TableLoader:
    def __init__(self):
        pass

    def load(self, table, cols, start, end=None):
        DbUtils.reset_table(table, cols)
        self.load_matches(table, start, end)
        self.verify_table(table)

    @staticmethod
    def load_matches(table, start, end=None):
        yr = start
        if end is None:
            end = start
        print(f"Loading matches from {start} - {end}")
        sqlite_obj = SqliteOperator(cn.db_folder, cn.db_file)
        while yr <= end:
            print("\n\n")
            print(yr)
            sqlite_obj.add_year_to_table(yr, table)
            yr += 1

    @staticmethod
    def verify_table(table):
        query = f"""
        SELECT *
        FROM {table}
        WHERE score != 'W/O'
        ORDER BY score DESC
        LIMIT 50
        """
        res = DbUtils.run_query(query, get_df=True,verbose=True)
        df_print(res)

if __name__ == "__main__":
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    loader = TableLoader()
    loader.load("wta_matches_raw",cn.added_cols+cn.csv_cols, 1968,2022)
    loader.verify_table("wta_matches_raw")


# ï¿½
# def get_player_table():
#     query = """
#     SELECT
#         player_name,
#         group_concat(distinct player_id) as player_id_agg,
#         min(min_tourn_date) as min_tourn_date,
#         max(max_tourn_date) as max_tourn_date,
#         sum(matches) as total_matches

#         FROM (
#             SELECT
#                 winner_id as player_id,
#                 winner_name as player_name,
#                 min(tourney_date) as min_tourn_date,
#                 max(tourney_date) as max_tourn_date,
#                 count(*) as matches
#             FROM wta_matches
#             GROUP BY player_id, player_name
#             UNION

#             SELECT
#                 loser_id as player_id,
#                 loser_name as player_name,
#                 min(tourney_date) as min_tourn_date,
#                 max(tourney_date) as max_tourn_date,
#                 count(*) as matches
#             FROM wta_matches
#             GROUP BY player_id, player_name
#         )
#         GROUP BY player_name
#     """
#     # sqlite_obj = SqliteOperator(cn.db_folder, cn.db_file)
#     con = SqliteOperator.get_sqlite_connector(cn.db_folder,cn.db_file)
#     player_df = pd.read_sql(query,con)

#     player_df['player_id_agg'] = player_df.player_id_agg.str.split(',')
#     player_df['new_id'] = player_df.player_id_agg.apply(min)
#     player_df['old_id'] = player_df.player_id_agg.apply(max)
#     player_df['repeat_flag'] = player_df.player_id_agg.apply(len) > 1
#     repeated_id_df = player_df[player_df['repeat_flag'] == True].copy()
#     output_path = os.path.join("outputs","wta_player_id_mapping.csv")
#     repeated_id_df = repeated_id_df[['old_id','new_id']]
#     repeated_id_df.to_csv(output_path,index=False)
#     con.close()
#     # loser_df = pd.read_sql(query_template.format(st='loser'),con)
#     # df_print(query_df)
#     return True

# def get_player_id_info():
#     query = """
#     SELECT
#         player_name,
#         player_id,
#         min(min_tourn_date) as min_tourn_date,
#         max(max_tourn_date) as max_tourn_date,
#         sum(matches) as total_matches

#         FROM (
#             SELECT
#                 winner_id as player_id,
#                 winner_name as player_name,
#                 min(tourney_date) as min_tourn_date,
#                 max(tourney_date) as max_tourn_date,
#                 count(*) as matches
#             FROM wta_matches
#             GROUP BY player_id, player_name
#             UNION

#             SELECT
#                 loser_id as player_id,
#                 loser_name as player_name,
#                 min(tourney_date) as min_tourn_date,
#                 max(tourney_date) as max_tourn_date,
#                 count(*) as matches
#             FROM wta_matches
#             GROUP BY player_id, player_name
#         )
#         GROUP BY player_name, player_id
#     """
#     # sqlite_obj = SqliteOperator(cn.db_folder, cn.db_file)
#     con = SqliteOperator.get_sqlite_connector(cn.db_folder,cn.db_file)
#     player_df = pd.read_sql(query,con)
#     player_df['player_id_arr'] = player_df.player_id_agg.str.split(',')
#     # player_df['player_id'] = player_df.player_id_agg.apply(min)
#     # player_df['num_ids'] = player_df.player_id_agg.apply(len)
#     # player_df['flag'] = player_df.num_ids > 2
#     # repeated_id_df = player_df[player_df['repeat_flag']].copy()
#     output_path = os.path.join("outputs","wta_players_repeats.csv")
#     player_df.to_csv(output_path,index=False)
#     con.close()
#     # loser_df = pd.read_sql(query_template.format(st='loser'),con)
#     # df_print(query_df)
#     return True







# a = MatchLoader("old_matches","wta")
# tour_df, qual_df = a.load_matches(1986)
# all_matches_df = pd.concat([tour_df, qual_df],axis=0,ignore_index=True)
# print(all_matches_df.columns)
# with pd.option_context("display.max_columns", None, "display.max_rows", None):
    # print(all_matches_df.groupby(['match_id'])['match_id'].count().sort_values(ascending=False))
# df_print(all_matches_df[all_matches_df.score.isna()])
# load_matches(1968,2022)

# print(DbUtils.run_query("SELECT COUNT(*) FROM wta_matches", get_df=False))

# print(DbUtils.check_table_exists("spam"))
# print(DbUtils.check_table_exists("wta_matches"))
# print(DbUtils.get_table_names())
# res = DbUtils.get_table_names()
# player_id_map = csv_to_dict(os.path.join("outputs","wta_player_id_mapping.csv"),"old_id","new_id")
# print({'a':player_id_map, 'b':player_id_map})

# con = SqliteOperator.get_sqlite_connector(cn.db_folder,cn.db_file)
# cur = con.cursor()
# res = cur.execute("SELECT max(tourney_date) FROM matches")
# print("\n\n")
# print(len(res.fetchall()))
# print("\n\n")
# print("\n".join([str(x) for x in res.fetchall()]))