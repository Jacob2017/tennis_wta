from utils import MatchLoader, csv_to_dict
import pandas as pd
import constants as cn

# a, b = load_matches(2000,2020)

wta = MatchLoader("current_matches", "wta")

tour_matches_df, qual_matches_df = wta.load_matches(2000)

rankings_df = pd.DataFrame(columns=['tourney_date','player_name','rating_start','Ne','m','k_factor','total_score','avg_score','dp','performance_rating','expected_score','update','rating_end'])
DP_LOOKUP = csv_to_dict("dp_lookup.csv","p","dp")

print(tour_matches_df['tourney_level'].unique())
print(qual_matches_df['tourney_level'].unique())

def get_first_rating(level):
    if level == 1:
        return cn.main_tour_new
    elif level == 2:
        return cn.chal_tour_new
    elif level == 3:
        return cn.itf_tour_new
    elif level == 4:
        return cn.qual_tour_new

# print(tour_matches_df.columns)
def one_match_elo_expect(r_a, r_b):
    return 1 / (1 + 10 ** ((r_b - r_a)/400))

def run_date(date, matches_df, rankings_df, level=1):
    matches_df = matches_df[matches_df['tourney_date'] == date]
    for player in matches_df['winner_name'].unique():
        player_df = matches_df[(matches_df['winner_name'] == player) | (matches_df['loser_name'] == player)]
        player_rank_df = rankings_df[(rankings_df['player_name']==player) & (rankings_df['tourney_date'] >= date - 10000)]
        if len(player_rank_df) != 0:
            max_rank = player_rank_df[player_rank_df['tourney_date']==max(player_rank_df['tourney_date'])]
        else:
            max_rank = None
        with pd.option_context('display.max_columns', None, 'display.max_rows', None):
            print(player_df)
            print(max_rank)
        tourney_date = date
        rating_start = rankings_df
        if max_rank is None:
            rating_start = get_first_rating(level)
            ne = 0
        else:
            rating_start = max_rank.at[0,'rating_end']
            ne = player_rank_df['m'].sum()
        m = len(player_df)
        k_factor = 800 / (ne + m + 8)
        total_score = player_df[player_df['winner_name'] == player]['s1'].sum() + player_df[player_df['loser_name']['s2']].sum()
        avg_score = total_score / m
        dp = DP_LOOKUP[round(avg_score,2)]
        opponents = list(matches_df[matches_df['winner_name']==player]['loser_name']) + list(matches_df[matches_df['loser_name']==player]['winner_name'])
        if len(rankings_df) > 0:
            opponents_rankings = list(rankings_df[(rankings_df['player_name'].isin(opponents)) &
                                             (rankings_df['tourney_date'] == max(rankings_df['tourney_date']))]['rating_end'])
        else:
            opponents_rankings = []
        
        while len(opponents_rankings) < len(opponents):
            opponents_rankings.append(get_first_rating(level))

        avg_rating = sum(opponents_rankings) / len(opponents_rankings)
        
        expected_total = 0
        for opp in opponents_rankings:
            expected_total += one_match_elo_expect(rating_start, opp)
        update = k_factor * (total_score - expected_total)
        new_rating = rating_start + update
        

        
        
        print(player)
        # print(matches_df[matches_df['match_num'] == min(matches_df['match_num'])])
        break