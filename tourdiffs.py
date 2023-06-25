import pandas as pd
import constants as cn
import os
from utils import MatchLoader

# Separate to new file for working out tour/qual difference
m = MatchLoader()

tour_matches_df, qual_matches_df = m.load_matches(2000,2009)


player_tour_map = {}

tourn_dates = set(qual_matches_df['tourney_date'].unique())
tourn_dates.update(list(tour_matches_df['tourney_date'].unique()))
tourn_dates = sorted(list(tourn_dates))

for d in tourn_dates:
    # print("\n\n")
    # print(d)
    qual_date_df = qual_matches_df[qual_matches_df['tourney_date']==d]
    tour_date_df = tour_matches_df[tour_matches_df['tourney_date']==d]

    q_players = sorted(list(pd.concat(
        [qual_date_df['winner_id'],qual_date_df['loser_id']], ignore_index=True
        ).unique()))
    # print([x for x in q_players if x in player_tour_df['player_id']])
    q_players = {x: 'qual' for x in q_players if x not in player_tour_map.keys()}
    # print(q_players)

    t_players = sorted(list(pd.concat(
        [tour_date_df['winner_id'], tour_date_df['loser_id']], ignore_index=True
        ).unique()))
    # print([x for x in t_players if x in player_tour_df['player_id']])
    t_players = [x for x in t_players if x not in q_players.keys()]
    t_players = {x: 'tour' for x in t_players if x not in player_tour_map.keys()}
    # print(t_players)

    player_tour_map = {**player_tour_map,
                       **q_players,
                       **t_players}


# with pd.option_context('display.max_columns', None, 'display.max_rows', None):
#     print(player_tour_df.sort_values('player_id'))

all_matches_df = pd.concat([tour_matches_df, qual_matches_df], axis=0, ignore_index=True)
all_matches_df['w_tour'] = all_matches_df['winner_id'].map(player_tour_map)
all_matches_df['l_tour'] = all_matches_df['loser_id'].map(player_tour_map)

cross_tour_matches_df = all_matches_df[all_matches_df['w_tour'] != all_matches_df['l_tour']]


tour_wins_df = cross_tour_matches_df[cross_tour_matches_df['w_tour']=='tour']
qual_wins_df = cross_tour_matches_df[cross_tour_matches_df['w_tour']=='qual']

with pd.option_context('display.max_columns', None, 'display.max_rows', 10):
    print(qual_wins_df)

print(len(cross_tour_matches_df))
print(len(tour_wins_df))
print(len(qual_wins_df))
print(f"Tour Win %: {(len(tour_wins_df) * 100.0)/ len(cross_tour_matches_df)}")