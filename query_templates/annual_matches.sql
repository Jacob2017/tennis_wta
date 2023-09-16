SELECT *
FROM wta_matches_raw
WHERE (tourney_date >= date '@year-01-01') and (tourney_date <= date '@year-12-31')