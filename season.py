from sqlite_operator import SqliteOperator
from db_utils import DbUtils
from utils import df_print

class Season:
    def __init__(self, year):
        self.year = year

    def run_year(self):
        tourn_df = self.get_annual_tournaments(self.year)

    @staticmethod
    def get_annual_tournaments(year):
        query_template = SqliteOperator.get_sql_file("annual_tournaments.sql","query_templates")
        tourn_query = query_template.replace("@year",str(year))
        tourn_df = DbUtils.run_query(tourn_query, get_df=True)
        df_print(tourn_df)
        return tourn_df
