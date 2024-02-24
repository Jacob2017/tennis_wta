SELECT match_id
    ,tourney_id
    ,match_num
    ,round
    ,winner_name
    ,loser_name
    ,score
    ,tourney_name
    ,tourney_date
    ,tourney_level
    ,draw_size
    ,winner_id
    ,loser_id
    ,best_of
    ,tourney_group
    ,draw_str
    ,season
    ,level
FROM wta_matches_raw
WHERE tourney_date = '@date'
AND tourney_id = '@id'
AND tourney_name = '@name'
