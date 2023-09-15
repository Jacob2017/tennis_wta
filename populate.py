from sqlite_operator import SqliteOperator
from utils import csv_to_dict, df_print
import constants as cn
import pandas as pd
import os
from db_utils import DbUtils



def load_matches(start, end=None):
    yr = start
    if end is None:
        end = start
    print(f"Loading matches from {start} - {end}")
    sqlite_obj = SqliteOperator(cn.db_folder, cn.db_file)
    while yr <= end:
        print("\n\n")
        print(yr)
        sqlite_obj.add_year_to_table(yr,"wta_matches")
        yr += 1

DbUtils.reset_table("wta_matches",cn.output_cols)
load_matches(1968,2022)

def verify_table():
    query = """
    SELECT *
    FROM wta_matches
    ORDER BY s2 DESC
    LIMIT 50
    """

    res = DbUtils.run_query(query, get_df=True,verbose=True)
    df_print(res)

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