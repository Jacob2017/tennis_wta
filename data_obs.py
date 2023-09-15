import pandas as pd
from utils import MatchLoader

wta = MatchLoader("current_matches", "wta")

tour_matches_df, qual_matches_df = wta.load_matches(2000)

print(tour_matches_df.columns)
