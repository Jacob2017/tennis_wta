import polars as pl
import io, os, sys
import constants as cn

# sys.stdout.encoding = 'utf-8'

def load_matches(year):
    """
    Load the WTA match files for a certain year.
    """

    folder = "current_matches"
    wta_template = "wta_matches_{}.csv"
    qual_itf_template = "wta_matches_qual_itf_{}.csv"

    keep_cols = ['tourney_id','tourney_name', 'surface', 'draw_size', 'tourney_level',
                 'tourney_date', 'match_num', 'winner_name', 'winner_id', 'loser_name', 
                 'loser_id', 'score', 'best_of', 'round']
    # keep_cols = [keep_cols[0]]

    main_df = pl.read_csv(os.path.join(folder,wta_template.format(year)),
                        dtypes=cn.csv_dtypes,
                        columns=keep_cols,
                        n_rows=100
                        #   ignore_errors=True
                        # infer_schema_length=1000
                        )
    # qual_df = pl.read_csv(os.path.join(folder,qual_itf_template.format(year)),
    #                       dtypes=cn.csv_dtypes)

    
    
    # identify_encoding_issue(main_df)

    # print(main_df)

    # return main_df.select([keep_cols]), qual_df.select([keep_cols])
    return main_df

def parse_scores(score):
    set_scores = score.split(" ")
    output_games = []
    for set in set_scores:
        output_games.append(set[0])
        output_games.append(set[2])
    while len(output_games) < 10:
        output_games.append(0)
    return output_games


def polar_prep(df):
    score_cols = ['w_set1', 'l_set1', 'w_set2', 'l_set2', 'w_set3', 'l_set3', 'w_set4', 'l_set4',
                  'w_set5', 'l_set5']

    df = df.with_columns(
        pl.col('score').apply(parse_scores).alias('game_scores')
    )

    for i, col in enumerate(score_cols):
        df = df.with_columns(
            pl.col('game_scores').apply(lambda s: int(s[i]) if (i < len(s) and s[i] is not None) else 0).alias(col)        
        )
        

    df = df.with_columns(
        winner_games=pl.expr.list_sum([df[col] for col in score_cols if col.startswith('w_set')]),
        loser_games=pl.expr.list_sum([df[col] for col in score_cols if col.startswith('l_set')]),
        total_games=pl.expr.list_sum(df['game_scores']),
        s1=pl.round(0.25 + 0.75 * (pl.col('winner_games') / pl.col('total_games')), 2),
        s2=pl.round(0.75 * (pl.col('loser_games') / pl.col('total_games')), 2)
    )
    return df

# # Example usage:
# df = pl.DataFrame({
#     'score': ["6-3 7-6(5)", "4-6 6-4 7-5"]
# })

# df = prep_df(df)
# print(df)

if __name__ == "__main__":
    display_cols = ["tourney_name","match_num","winner_name","loser_name","score","sets_list"]
    a = load_matches("2000")
    a = polar_prep(a)
    with pl.Config(tbl_cols=1000):
        print(a.select(pl.col(display_cols)))

def prep_df(df):
    score_cols = ['w_set1', 'l_set1', 'w_set2', 'l_set2', 'w_set3', 'l_set3', 'w_set4', 'l_set4',
              'w_set5', 'l_set5']

    df['w_set1'], df['l_set1'], df['w_set2'], df['l_set2'], df['w_set3'], df['l_set3'], df['w_set4'],\
    df['l_set4'], df['w_set5'], df['l_set5'] = zip(*df['score'].map(parse_scores))

    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').convert_dtypes().fillna(0)

    df['winner_games'], df['loser_games'], df['total_games'] = zip(*df.apply(get_total_games, axis=1))
    df['s1'] = round(0.25 + 0.75*(df['winner_games'] / df['total_games']), 2)
    df['s2'] = round(0.75*(df['loser_games'] / df['total_games']), 2)

    return df

def extract_scores(df):
    out = df.with_columns(
        [
            pl.col("score")
            .str.extract_all(
                r'\d+(?![^(]*\))'
            )
        ]
    )
    # out = out.explode("sets_list")
    return out



    

    

def parse_scores(score):
    set_scores = score.split(" ")
    output_games = []
    for set in set_scores:
        output_games.append(set[0])
        output_games.append(set[2])
    while len(output_games) < 10:
        output_games.append(0)
    return output_games

def get_total_games(row):
    winner_total = row['w_set1'] + row['w_set2'] + row['w_set3'] + row['w_set4'] + row['w_set5']
    loser_total = row['l_set1'] + row['l_set2'] + row['l_set3'] + row['l_set4'] + row['l_set5']
    return winner_total, loser_total, winner_total+loser_total

def get_elo_score(row):
    winner_total = row['w_set1'] + row['w_set2'] + row['w_set3'] + row['w_set4'] + row['w_set5']
    loser_total = row['l_set1'] + row['l_set2'] + row['l_set3'] + row['l_set4'] + row['l_set5']
    return 0.5 + 0.5 * (winner_total / (winner_total + loser_total)), 0.5 * (loser_total / (winner_total+loser_total))



def get_first_rating(level):
    if level == 1:
        return 1500
    elif level == 2:
        return 1250
    elif level == 3:
        return 1000

def load_matches_range(start,end):
    yr = start
    tour_matches_df = None
    qual_matches_df = None

    while yr <= end:
        a, b = load_matches(str(yr))
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



# tour_matches_df, qual_matches_df = load_matches_range(2000,2009)

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
    # new_rankings_df = pd.DataFrame.from_dict(new_rankings_dict)

# dp_lookup_df = pd.read_csv("dp_lookup.csv")
def one_match_elo_expect(r_a, r_b):
    return 1 / (1 + 10 ** ((r_b - r_a)/400))


# rankings_df = pd.DataFrame(columns=['tourney_date','player_name','rating_start','Ne','m','k_factor','total_score','avg_score','dp','performance_rating','expected_score','update','rating_end'])

# run_date(20000103, tour_matches_df, rankings_df, 2)

# with pd.option_context('display.max_columns', None, 'display.max_rows', None):
#     # print(tour_matches_df['winner_name'].nunique())
#     # print(tour_matches_df['loser_name'].nunique())
#     # print(qual_matches_df['winner_name'].nunique())
#     # print(qual_matches_df['loser_name'].nunique())

#     pass
    # print(tour_matches_df['tourney_level'].unique())
    # print(qual_matches_df['tourney_level'].unique())

    # quals_only = qual_matches_df[qual_matches_df['tourney_level'].isin(['G','T1','T2','T3','T4'])]
    # print(quals_only[quals_only['tourney_date']==min(quals_only['tourney_date'])])


    # print(tour_matches_df[tour_matches_df['tourney_date']==min(tour_matches_df['tourney_date'])])
    # print(qual_matches_df[qual_matches_df['tourney_date']==min(qual_matches_df['tourney_date'])])
    # print(a)
    # print(a.dtypes)

## Separate to new file for working out tour/qual difference

# player_tour_map = {}

# tourn_dates = set(qual_matches_df['tourney_date'].unique())
# tourn_dates.update(list(tour_matches_df['tourney_date'].unique()))
# tourn_dates = sorted(list(tourn_dates))

# for d in tourn_dates:
#     # print("\n\n")
#     # print(d)
#     qual_date_df = qual_matches_df[qual_matches_df['tourney_date']==d]
#     tour_date_df = tour_matches_df[tour_matches_df['tourney_date']==d]

#     q_players = sorted(list(pd.concat(
#         [qual_date_df['winner_id'],qual_date_df['loser_id']], ignore_index=True
#         ).unique()))
#     # print([x for x in q_players if x in player_tour_df['player_id']])
#     q_players = {x: 'qual' for x in q_players if x not in player_tour_map.keys()}
#     # print(q_players)

#     t_players = sorted(list(pd.concat(
#         [tour_date_df['winner_id'], tour_date_df['loser_id']], ignore_index=True
#         ).unique()))
#     # print([x for x in t_players if x in player_tour_df['player_id']])
#     t_players = [x for x in t_players if x not in q_players.keys()]
#     t_players = {x: 'tour' for x in t_players if x not in player_tour_map.keys()}
#     # print(t_players)

#     player_tour_map = {**player_tour_map,
#                        **q_players,
#                        **t_players}


# # with pd.option_context('display.max_columns', None, 'display.max_rows', None):
# #     print(player_tour_df.sort_values('player_id'))

# all_matches_df = pd.concat([tour_matches_df, qual_matches_df], axis=0, ignore_index=True)
# all_matches_df['w_tour'] = all_matches_df['winner_id'].map(player_tour_map)
# all_matches_df['l_tour'] = all_matches_df['loser_id'].map(player_tour_map)

# cross_tour_matches_df = all_matches_df[all_matches_df['w_tour'] != all_matches_df['l_tour']]


# tour_wins_df = cross_tour_matches_df[cross_tour_matches_df['w_tour']=='tour']
# qual_wins_df = cross_tour_matches_df[cross_tour_matches_df['w_tour']=='qual']

# with pd.option_context('display.max_columns', None, 'display.max_rows', 10):
#     print(qual_wins_df)

# print(len(cross_tour_matches_df))
# print(len(tour_wins_df))
# print(len(qual_wins_df))
# print(f"Tour Win %: {(len(tour_wins_df) * 100.0)/ len(cross_tour_matches_df)}")
    
    
