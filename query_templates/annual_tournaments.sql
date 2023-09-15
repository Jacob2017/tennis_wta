SELECT tourney_id
    ,tourney_name
    ,tourney_date
    ,tourney_level
    ,surface
    ,year
    ,count(*) as matches 
FROM wta_matches
WHERE year = @year
GROUP BY tourney_id
    ,tourney_name
    ,tourney_date
    ,tourney_level
    ,surface
    ,year
ORDER BY tourney_date
        ,tourney_id