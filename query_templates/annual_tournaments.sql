SELECT tourney_date as tourn_date
    ,group_concat(distinct tourney_id) as tourn_id_agg
    ,group_concat(distinct tourney_name) as tourn_name_agg
FROM wta_matches_raw
WHERE season = @year
GROUP BY tourney_date
ORDER BY tourney_date