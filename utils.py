import csv
import pandas as pd

def csv_to_dict(filename, key_column, value_column):
    result = {}
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row[key_column]
            value = row[value_column]
            result[key] = value

    return result


def df_print(df):
    # temp_df = df[cn.print_cols]
    with pd.option_context("display.max_columns", None, "display.max_rows", None):
        print(df)


# run_date(20000103, tour_matches_df, rankings_df, 2)


# print(tour_matches_df['winner_name'].nunique())
# print(tour_matches_df['loser_name'].nunique())
# print(qual_matches_df['winner_name'].nunique())
# print(qual_matches_df['loser_name'].nunique())


# print(tour_matches_df['tourney_level'].unique())
# print(qual_matches_df['tourney_level'].unique())

# quals_only = qual_matches_df[qual_matches_df['tourney_level'].isin(['G','T1','T2','T3','T4'])]
# print(quals_only[quals_only['tourney_date']==min(quals_only['tourney_date'])])


# print(tour_matches_df[tour_matches_df['tourney_date']==min(tour_matches_df['tourney_date'])])
# print(qual_matches_df[qual_matches_df['tourney_date']==min(qual_matches_df['tourney_date'])])
# print(a)
# print(a.dtypes)
