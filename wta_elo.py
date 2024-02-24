from sqlite_operator import SqliteOperator
from tournament.tournament_main import Tournament
from db_utils import DbUtils
from utils import df_print

class WtaElo:
    def __init__(self):
        pass

    @staticmethod
    def run_seasons(start,end=None):
        if end is None:
            end = start
        yr = start
        while yr <= end:
            WtaElo.run_year(yr)
            yr += 1

    @staticmethod
    def run_year(year):
        tourn_df = WtaElo.get_annual_tournaments(year)
        for row in tourn_df.iterrows():
            values = row[1]
            # print(len(values['tourn_name_agg'])==len(values['tourn_id_agg']))
            for tourn_name, tourn_id in zip(values['tourn_name_agg'], values['tourn_id_agg']):
                tourn_obj = Tournament(tourn_id, tourn_name, values['tourn_date'])
                # tourn_obj.print_tournament()
                tourn_obj.run_tournament()
            break

    @staticmethod
    def get_annual_tournaments(year):
        query_template = SqliteOperator.get_sql_file("annual_tournaments.sql","query_templates")
        tourn_query = query_template.replace("@year",str(year))
        tourn_df = DbUtils.run_query(tourn_query, get_df=True)
        tourn_df['tourn_name_agg'] = tourn_df['tourn_name_agg'].str.split(',')
        tourn_df['tourn_id_agg'] = tourn_df['tourn_id_agg'].str.split(',')
        return tourn_df

    

if __name__ == "__main__":
    wta_obj = WtaElo()
    wta_obj.run_seasons(2022)