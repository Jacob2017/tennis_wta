import pandas as pd
import constants as cn
import os

class MatchLoader:
    def __init__(self, folder, tour):
        self.folder = folder
        self.tour = tour

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
                tour_matches_df = pd.concat([tour_matches_df, a], axis=0, ignore_index=True)
            if qual_matches_df is None:
                qual_matches_df = b
            else:
                qual_matches_df = pd.concat([qual_matches_df, b], axis=0, ignore_index=True)

            yr += 1

        return tour_matches_df, qual_matches_df

    def _load_matches_single(self, year):
        """
        Load the relevant tour's match files for a certain year.
        """
        template = "{}_matches_{}.csv"
        # qual_itf_template = "{}_matches_qual_itf_{}.csv"

        main_df = pd.read_csv(os.path.join(self.folder,template.format(self.tour, year)))
        qual_df = pd.read_csv(os.path.join(self.folder,template.format(self.tour, "qual_itf_"+year)))

        keep_cols = ['tourney_id','tourney_name', 'surface', 'draw_size', 'tourney_level',
                    'tourney_date', 'match_num', 'winner_name', 'winner_id', 'loser_name', 
                    'loser_id', 'score', 'best_of', 'round']

        return main_df[keep_cols], qual_df[keep_cols]

    @staticmethod
    def parse_scores(score):
        set_scores = score.split(" ")
        output_games = []
        for set in set_scores:
            output_games.append(set[0])
            output_games.append(set[2])
        while len(output_games) < 10:
            output_games.append(0)
        return output_games
    
    @staticmethod
    def get_total_games(row):
        winner_total = row['w_set1'] + row['w_set2'] + row['w_set3'] + row['w_set4'] + row['w_set5']
        loser_total = row['l_set1'] + row['l_set2'] + row['l_set3'] + row['l_set4'] + row['l_set5']
        return winner_total, loser_total, winner_total+loser_total

    @staticmethod
    def get_elo_score(row):
        winner_total = row['w_set1'] + row['w_set2'] + row['w_set3'] + row['w_set4'] + row['w_set5']
        loser_total = row['l_set1'] + row['l_set2'] + row['l_set3'] + row['l_set4'] + row['l_set5']
        return 0.5 + 0.5 * (winner_total / (winner_total + loser_total)), 0.5 * (loser_total / (winner_total+loser_total))

    def prep_df(self, df):
        score_cols = ['w_set1', 'l_set1', 'w_set2', 'l_set2', 'w_set3', 'l_set3', 'w_set4', 'l_set4',
                'w_set5', 'l_set5']

        df['w_set1'], df['l_set1'], df['w_set2'], df['l_set2'], df['w_set3'], df['l_set3'], df['w_set4'],\
        df['l_set4'], df['w_set5'], df['l_set5'] = zip(*df['score'].map(self.parse_scores))

        for col in score_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').convert_dtypes().fillna(0)

        df['winner_games'], df['loser_games'], df['total_games'] = zip(*df.apply(self.get_total_games, axis=1))
        df['s1'] = round(0.25 + 0.75*(df['winner_games'] / df['total_games']), 2)
        df['s2'] = round(0.75*(df['loser_games'] / df['total_games']), 2)

        return df

def get_first_rating(level):
        if level == 1:
            return cn.main_tour_new
        elif level == 2:
            return cn.chal_tour_new
        elif level == 3:
            return cn.itf_tour_new
        elif level == 4:
            return cn.qual_tour_new

    # new_rankings_df = pd.DataFrame.from_dict(new_rankings_dict)

dp_lookup_df = pd.read_csv("dp_lookup.csv")
def one_match_elo_expect(r_a, r_b):
    return 1 / (1 + 10 ** ((r_b - r_a)/400))


rankings_df = pd.DataFrame(columns=['tourney_date','player_name','rating_start','Ne','m','k_factor','total_score','avg_score','dp','performance_rating','expected_score','update','rating_end'])

# run_date(20000103, tour_matches_df, rankings_df, 2)

with pd.option_context('display.max_columns', None, 'display.max_rows', None):
    # print(tour_matches_df['winner_name'].nunique())
    # print(tour_matches_df['loser_name'].nunique())
    # print(qual_matches_df['winner_name'].nunique())
    # print(qual_matches_df['loser_name'].nunique())

    pass
    # print(tour_matches_df['tourney_level'].unique())
    # print(qual_matches_df['tourney_level'].unique())

    # quals_only = qual_matches_df[qual_matches_df['tourney_level'].isin(['G','T1','T2','T3','T4'])]
    # print(quals_only[quals_only['tourney_date']==min(quals_only['tourney_date'])])


    # print(tour_matches_df[tour_matches_df['tourney_date']==min(tour_matches_df['tourney_date'])])
    # print(qual_matches_df[qual_matches_df['tourney_date']==min(qual_matches_df['tourney_date'])])
    # print(a)
    # print(a.dtypes)


    
    
