import constants as cn
import pandas as pd
import numpy as np
import os
import chardet
from utils import csv_to_dict

class MatchLoader:
    """
    Utility class to load matches from CSV.
    """

    def __init__(self, folder, tour):
        self.folder = folder
        self.tour = tour.lower()

    def load_matches(self, start, end=None):
        yr = start
        if end is None:
            end = start
        tour_matches_df = None
        qual_matches_df = None

        while yr <= end:
            a, b = self._load_matches_single(str(yr))
            if tour_matches_df is None:
                tour_matches_df = a
            else:
                tour_matches_df = pd.concat(
                    [tour_matches_df, a], axis=0, ignore_index=True
                )
            if qual_matches_df is None:
                qual_matches_df = b
            else:
                qual_matches_df = pd.concat(
                    [qual_matches_df, b], axis=0, ignore_index=True
                )

            yr += 1

        if sum(tour_matches_df.score.isna()) > 0:
            print(f"Dropping {sum(tour_matches_df.score.isna())} rows from Main Tour {start} - {end} for nulls.")
        if sum(qual_matches_df.score.isna()) > 0:
            print(f"Dropping {sum(qual_matches_df.score.isna())} rows from Qual Tour {start} - {end} for nulls.")
        tour_matches_df.dropna(subset=['score'],
                               axis=0, inplace=True)
        qual_matches_df.dropna(subset=['score'],
                               axis=0, inplace=True)

        if len(tour_matches_df) > 0:
            tour_matches_df = self.prep_df(tour_matches_df)
        if len(qual_matches_df) > 0:
            qual_matches_df = self.prep_df(qual_matches_df)

        return tour_matches_df, qual_matches_df

    def _load_matches_single(self, year):
        """
        Load the relevant tour's match files for a certain year.
        """
        template = "{}_matches_{}.csv"
        # qual_itf_template = "{}_matches_qual_itf_{}.csv"
        # keep_cols = [
        #     "tourney_id",
        #     "tourney_name",
        #     "surface",
        #     "draw_size",
        #     "tourney_level",
        #     "tourney_date",
        #     "match_num",
        #     "winner_name",
        #     "winner_id",
        #     "loser_name",
        #     "loser_id",
        #     "score",
        #     "best_of",
        #     "round",
        #     "year",
        #     "level"
        # ]
        try:
            with open(os.path.join(self.folder, template.format(self.tour, year)), 'rb') as f:
                result = chardet.detect(f.read())
            main_df = pd.read_csv(os.path.join(self.folder, template.format(self.tour, year)), 
                                    encoding=result['encoding'])
        except FileNotFoundError:
            print(f"No file available: {template.format(self.tour,year)}")
            main_df = pd.DataFrame(columns=cn.added_cols+cn.csv_cols)

        try:
            with open(os.path.join(self.folder, template.format(self.tour, "qual_itf_" + year)), 'rb') as f:
                result = chardet.detect(f.read())

            qual_df = pd.read_csv(os.path.join(self.folder, template.format(self.tour, "qual_itf_" + year)), 
                             encoding=result['encoding'])
        except FileNotFoundError:
            print(f"No file available: {template.format(self.tour, 'qual_itf_' + year)}")
            qual_df = pd.DataFrame(columns=cn.output_cols)            
        
        main_df['season'] = [int(year)] * len(main_df)
        main_df['level'] = ['Main'] * len(main_df)
        qual_df['season'] = [int(year)] * len(qual_df)
        qual_df['level'] = ['Lower'] * len(qual_df)

        return main_df, qual_df
    
    @staticmethod
    def prep_df(df):
        # score_cols = [
        #     "w_set1",
        #     "l_set1",
        #     "w_set2",
        #     "l_set2",
        #     "w_set3",
        #     "l_set3",
        #     "w_set4",
        #     "l_set4",
        #     "w_set5",
        #     "l_set5",
        # ]

        # (
        #     df["w_set1"],
        #     df["l_set1"],
        #     df["w_set2"],
        #     df["l_set2"],
        #     df["w_set3"],
        #     df["l_set3"],
        #     df["w_set4"],
        #     df["l_set4"],
        #     df["w_set5"],
        #     df["l_set5"],
        # ) = zip(*df["score"].map(MatchLoader.parse_scores))

        # for col in score_cols:
        #     df[col] = pd.to_numeric(df[col], errors="coerce").convert_dtypes().fillna(0)

        # df["winner_games"], df["loser_games"], df["total_games"] = zip(
        #     *df.apply(MatchLoader.get_total_games, axis=1)
        # )
        # df["wo_flag"] = df["total_games"] == 0
        # df["short_match_flag"] = df["total_games"] <= 6
        # df["s1"] = round(0.25 + 0.75 * (df["winner_games"] / df["total_games"]), 2)
        # df["s2"] = round(0.75 * (df["loser_games"] / df["total_games"]), 2)
        
        df["tourney_group"] = df["tourney_level"].map(cn.tourn_code_map)
        df["draw_str"] = np.where(df["round"].isin(["Q1","Q2","Q3","Q4","Q5"]),"Q", "MD")
        df["match_id"] = df.tourney_id + "-" + df.draw_str + "-" + df.match_num.map('{:03d}'.format)
        df["tourney_date"] = pd.to_datetime(df.tourney_date,format="%Y%m%d")
        player_id_map = csv_to_dict(os.path.join("outputs","wta_player_id_mapping.csv"),"old_id","new_id")
        df.replace({'winner_id':player_id_map, 'loser_id':player_id_map}, inplace=True)
        # df = df[[x for x in cn.output_cols if x in df.columns]]
        return df

    @staticmethod
    def parse_scores(score):
        output_games = []
        try:
            set_scores = score.split(" ")
            for set in set_scores:
                if "-" not in set:
                    continue
                if len(set) >= 3:
                    tiebreak_flag = False
                    if "[" in set and "]" in set:
                        tiebreak_flag = True
                    set.replace("[","")
                    set.replace("]","")
                    split_score = set.split("-")
                    split_score[1] = split_score[1].split('(')[0]
                    if split_score[0].isdigit() and split_score[1].isdigit():
                        score1 = int(split_score[0])
                        score2 = int(split_score[1])
                        if score1 >= 10:
                            tiebreak_flag = True
                        if tiebreak_flag:
                            output_games.append(1)
                            output_games.append(0)
                        else:
                            output_games.append(score1)
                            output_games.append(score2)
                    else:
                        output_games.append(0)
                        output_games.append(0)
                else:
                    output_games.append(0)
                    output_games.append(0)
        except AttributeError as e:
            print(score)
        while len(output_games) < 10:
            output_games.append(0)
        return output_games

    @staticmethod
    def get_total_games(row):
        winner_total = (
            row["w_set1"]
            + row["w_set2"]
            + row["w_set3"]
            + row["w_set4"]
            + row["w_set5"]
        )
        loser_total = (
            row["l_set1"]
            + row["l_set2"]
            + row["l_set3"]
            + row["l_set4"]
            + row["l_set5"]
        )
        return winner_total, loser_total, winner_total + loser_total

    @staticmethod
    def get_elo_score(row):
        winner_total = (
            row["w_set1"]
            + row["w_set2"]
            + row["w_set3"]
            + row["w_set4"]
            + row["w_set5"]
        )
        loser_total = (
            row["l_set1"]
            + row["l_set2"]
            + row["l_set3"]
            + row["l_set4"]
            + row["l_set5"]
        )
        return (0.5 + 0.5 * (winner_total / (winner_total + loser_total)), 
                0.5 * (loser_total / (winner_total + loser_total)))
    # new_rankings_df = pd.DataFrame.from_dict(new_rankings_dict)