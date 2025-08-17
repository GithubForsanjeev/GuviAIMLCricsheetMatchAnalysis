-- 1. Top 10 batsmen by total runs in ODIs
SELECT batsman, SUM(runs) AS total_runs
FROM odi_deliveries
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;

-- 2. Top 10 wicket-takers in T20s
SELECT bowler, COUNT(*) AS wickets
FROM t20_deliveries
WHERE dismissal_type IN ('bowled', 'caught', 'lbw', 'stumped', 'hit wicket')
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10;

-- 3. Most sixes hit in Test matches
SELECT batsman, COUNT(*) AS sixes
FROM test_deliveries
WHERE runs = 6
GROUP BY batsman
ORDER BY sixes DESC
LIMIT 10;

-- 4. Best bowling average in ODIs (min 10 wickets)
SELECT bowler, SUM(runs_conceded) / COUNT(*) AS bowling_avg
FROM odi_deliveries
WHERE dismissal_type IS NOT NULL
GROUP BY bowler
HAVING COUNT(*) >= 10
ORDER BY bowling_avg ASC
LIMIT 10;

-- 5. Total centuries across all formats
SELECT match_type, COUNT(*) AS centuries
FROM player_innings
WHERE runs >= 100
GROUP BY match_type;

-- 6. Team with highest win percentage in Tests
SELECT team, 
       COUNT(*) FILTER (WHERE result = 'win') * 100.0 / COUNT(*) AS win_pct
FROM test_matches
GROUP BY team
ORDER BY win_pct DESC
LIMIT 1;

-- 7. Matches with narrowest margin of victory (by runs)
SELECT match_id, team_winner, margin
FROM match_results
WHERE win_type = 'runs'
ORDER BY margin ASC
LIMIT 5;

-- 8. Highest scoring ODI matches
SELECT match_id, SUM(runs) AS total_runs
FROM odi_deliveries
GROUP BY match_id
ORDER BY total_runs DESC
LIMIT 5;

-- 9. Most extras conceded in a T20 match
SELECT match_id, SUM(extras) AS total_extras
FROM t20_deliveries
GROUP BY match_id
ORDER BY total_extras DESC
LIMIT 5;

-- 10. Longest Test matches by number of deliveries
SELECT match_id, COUNT(*) AS total_deliveries
FROM test_deliveries
GROUP BY match_id
ORDER BY total_deliveries DESC
LIMIT 5;

-- 11. Most matches played by a player
SELECT player_name, COUNT(DISTINCT match_id) AS matches_played
FROM player_innings
GROUP BY player_name
ORDER BY matches_played DESC
LIMIT 10;

-- 12. Players with most ducks
SELECT player_name, COUNT(*) AS ducks
FROM player_innings
WHERE runs = 0
GROUP BY player_name
ORDER BY ducks DESC
LIMIT 10;

-- 13. Top strike rates in T20s (min 100 balls faced)
SELECT batsman, SUM(runs)*100.0 / COUNT(*) AS strike_rate
FROM t20_deliveries
GROUP BY batsman
HAVING COUNT(*) >= 100
ORDER BY strike_rate DESC
LIMIT 10;

-- 14. Economy rate of bowlers in ODIs (min 60 balls)
SELECT bowler, SUM(runs_conceded)*6.0 / COUNT(*) AS economy
FROM odi_deliveries
GROUP BY bowler
HAVING COUNT(*) >= 60
ORDER BY economy ASC
LIMIT 10;

-- 15. Most player-of-the-match awards
SELECT player_of_match, COUNT(*) AS awards
FROM match_info
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;

-- 16. Total matches played by each team across formats
SELECT team, COUNT(*) AS total_matches
FROM (
    SELECT team FROM test_matches
    UNION ALL
    SELECT team FROM odi_matches
    UNION ALL
    SELECT team FROM t20_matches
) AS all_matches
GROUP BY team
ORDER BY total_matches DESC;

-- 17. Win/loss ratio by team in ODIs
SELECT team, 
       COUNT(*) FILTER (WHERE result = 'win') AS wins,
       COUNT(*) FILTER (WHERE result = 'loss') AS losses,
       ROUND(CAST(COUNT(*) FILTER (WHERE result = 'win') AS FLOAT) / 
             NULLIF(COUNT(*) FILTER (WHERE result = 'loss'), 0), 2) AS win_loss_ratio
FROM odi_matches
GROUP BY team
ORDER BY win_loss_ratio DESC;

-- 18. Average first innings score in T20s
SELECT AVG(total_runs) AS avg_first_innings_score
FROM (
    SELECT match_id, SUM(runs) AS total_runs
    FROM t20_deliveries
    WHERE innings = 1
    GROUP BY match_id
) AS first_innings;

-- 19. Most common venues for ODIs
SELECT venue, COUNT(*) AS matches
FROM odi_matches
GROUP BY venue
ORDER BY matches DESC
LIMIT 10;

-- 20. Players with most appearances as captain
SELECT captain, COUNT(*) AS matches_as_captain
FROM match_info
GROUP BY captain
ORDER BY matches_as_captain DESC
LIMIT 10;