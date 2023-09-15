db_folder = "db"
db_file = "main.db"
main_tour_new = 1500
chal_tour_new = 1450
itf_tour_new = 1450
qual_tour_new = 1450
level_start_maps = {1: 1500, 2: 1450, 3: 1450, 4: 1450}
output_cols = ['match_id','tourney_id', 'tourney_name', 'tourney_date', 'tourney_level', 'draw_size',
               'score', 's1','s2','surface',  'match_num', 'winner_name', 'loser_name', 'winner_id',
               'loser_id', 'best_of', 'round', 'w_set1', 'l_set1', 'w_set2', 'l_set2', 'w_set3',
               'l_set3', 'w_set4', 'l_set4', 'w_set5', 'l_set5', 'winner_games', 'loser_games', 
               'total_games', 'wo_flag', 'short_match_flag', 'tourney_group', 'draw_str', 'year', 'level']
elo_cols = ['match_id','tourney_id','tourney_name','tourney_date','']
round_order = ["Q1","Q2","Q3","Q4","BR","RR","R256","R128","R64","R32","R16","QF","SF","F"]
print_cols = [
    "tourney_id",
    "tourney_name",
    "surface",
    "draw_size",
    "tourney_level",
    "tourney_date",
    "match_num",
    "winner_name",
    "winner_id",
    "loser_name",
    "loser_id",
    "score",
    "best_of",
    "round",
]
player_lookback = 12
tourn_code_map = {
    "D": 1,
    "CC": 1,
    "O": 1,
    "G": 1,
    "T1": 1,
    "T2": 1,
    "T3": 1,
    "T4": 1,
    "F": 1,
    "75": 2,
    "50": 2,
    "25": 3,
    "20": 3,
    "10": 3,
}
