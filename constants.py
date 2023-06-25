import polars as pl
main_tour_new = 1500
chal_tour_new = 1450
itf_tour_new = 1450
qual_tour_new = 1450
player_lookback = 12
tourn_code_map = {}
csv_dtypes = {
    'tourney_id': pl.Utf8, 
    'tourney_name': pl.Utf8, 
    'surface': pl.Utf8, 
    'draw_size': pl.UInt16, 
    'tourney_level': pl.Utf8,
    'tourney_date': pl.Utf8, 
    'match_num': pl.UInt16, 
    'winner_name': pl.Utf8, 
    'winner_id': pl.UInt32, 
    'loser_name': pl.Utf8,
    'loser_id': pl.UInt32, 
    'score': pl.Utf8, 
    'best_of': pl.UInt8, 
    'round': pl.Utf8
}