SELECT max(rank_date) as rank_date
FROM wta_elo_rank_weekly
WHERE rank_date <= @date