SELECT match_id
    ,tourney_id
    ,match_num
    ,round
    ,winner_name
    ,loser_name
    ,score
    ,s1
    ,s2
    ,tourney_name
    ,tourney_date
    ,tourney_level
    ,draw_size
    ,winner_id
    ,loser_id
    ,best_of
    ,wo_flag
    ,short_match_flag
    ,tourney_group
    ,draw_str
    ,year
    ,level
FROM wta_matches_raw
WHERE tourney_date = date '@date'
AND tourney_id = '@id'
AND tourney_name = '@name'
