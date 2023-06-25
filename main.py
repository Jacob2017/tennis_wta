from utils import MatchLoader
import pandas as pd
import constants as cn
import os


# a, b = load_matches(2000,2020)

m = MatchLoader()

tour_matches_df, qual_matches_df = m.load_matches(2000,2009)

# print(tour_matches_df.columns)


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
        dp = dp_lookup_df[dp_lookup_df['p']==avg_score].at[0,'dp']
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