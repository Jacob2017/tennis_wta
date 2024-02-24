- [x] Reload matches from csv
  - [x] 'Season' and 'Level' fields
  - [x] map repeated player IDs to old value

- [x] Check tournament loading works
- [ ] Set up match-loading and match-parsing - reuse some old match loader code
- [ ] Check tournament-match loading works

- [ ] Make match-loading use the raw columns provided
  - [ ] Need enough to make match_id column



Create delta table for each match.
Query last 365 to get elo delta per player on a given date (weekly)
Add to original ranking

rankings table schema:
* ranking date
* player id
* player name
* starting rating
* l52w elo delta
* starting rating
* total rating
* l52w matches

elo delta table schema (1 row per player per match):
* delta date
* match id
* player number in match - 1 = winner, 2 = loser
* player id
* player name
* prior elo rating
* opponent prior elo rating
* string score
* win/lose
* games won
* total games
* player elo score
* player expected elo score
* elo delta
* any match flags
  * short match (retirement)
  * walkover flag (elo delta = 0)


------
TOURNAMENT
    tournament_main
        Tournament
    PULL
        tournament_pull
            TournamentPull    
                get match data
                get latest player ratings
    STRUCTURE
        tournament_structure
            TournamentStructure
                join player ratings to matches


                structure to elo delta format
    ANALYSE
        tournament_analyse
            TournamentAnalyse
                Calculate expected elo
                Calculate elo delta
    OUTPUT?
        append to WTA elo delta table
        append to enriched matches table


