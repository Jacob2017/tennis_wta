SELECT tourney_id
    ,tourney_name
    ,tourney_date
    ,tourney_level
    ,surface
    ,season
    ,count(*) as matches 
FROM wta_matches_raw
WHERE season = @year
GROUP BY tourney_id
    ,tourney_name
    ,tourney_date
    ,tourney_level
    ,surface
    ,season
ORDER BY tourney_date
        ,tourney_id