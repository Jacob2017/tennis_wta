from datetime import datetime
from sqlite_operator import SqliteOperator
from db_utils import DbUtils
from tournament.pull.tournament_pull import TournamentPull
from utils import df_print

class Tournament:
    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date
        self.date_str = date[:10]

    def run_tournament(self):
        pull_obj = TournamentPull()
        pull_obj.pull_data()
        # matches_df = TournamentPull.get_matches(self.id, self.name, self.date)
        # players_df = TournamentPull.get_player_info_df(matches_df)

        # df_print(matches_df)
        df_print(players_df)

    

    def print_tournament(self):
        print(f"Welcome to {self.name} tournament, held on {self.date_str}.")
        # print(type(self.date))
    # def get_matches(name,)