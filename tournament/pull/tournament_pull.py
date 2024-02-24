from datetime import datetime
from sqlite_operator import SqliteOperator
from db_utils import DbUtils
import pandas as pd

class TournamentPull:
    def __init__(self):
        pass

    def pull_data(id,name,date):
        matches_df = TournamentPull.get_matches(id, name, date)
        ratings_df = TournamentPull.get_player_info_df(matches_df)

    @staticmethod
    def get_matches(id, name, date):
        query = SqliteOperator.get_sql_file("tournament_matches_raw.sql","query_templates")
        query = query.replace("@id", id)
        query = query.replace("@name",name)
        query = query.replace("@date",date)
        match_df = DbUtils.run_query(query, get_df=True)
        return match_df

    @staticmethod
    def get_player_ratings()
    
    @staticmethod
    def get_player_info_df(matches_df):
        winner_df = matches_df[['winner_id','winner_name']].copy()
        loser_df = matches_df[['loser_id','loser_name']].copy()
        winner_df.rename({'winner_id':'player_id', 'winner_name':'player_name'},axis=1,inplace=True)
        loser_df.rename({'loser_id':'player_id', 'loser_name':'player_name'},axis=1, inplace=True)
        player_df = pd.concat([winner_df,loser_df], axis=0, ignore_index=True)
        player_df.drop_duplicates(keep='first',inplace=True, ignore_index=True)
        return player_df.sort_values(by=['player_id'])


    @staticmethod
    def get_player_ratings(matches_df,date):
        pass