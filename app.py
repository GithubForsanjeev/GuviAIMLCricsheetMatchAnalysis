import streamlit as st
import pandas as pd
import sqlite3

#---function for run SQL query---
def run_query(query):
    connection = sqlite3.connect("cricket_matches.db") 
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result)         


st.header('🏏 Cricket Insights Dashboard')     #streamlit dashboard header

## Batting Insights

with st.expander("**01. Top 10 batsmen by total runs in ODIs**"):
    query = '''SELECT batter, SUM(runs_batter) AS total_runs
FROM odi_matches
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;'''
    st.write(run_query(query)) 


with st.expander("**02. Top 10 batsmen by strike rate in IPL (min 100 balls)**"):
    query = '''SELECT batter, ROUND(SUM(runs_batter) * 100.0 / COUNT(ball), 2) AS strike_rate
FROM t20_matches
GROUP BY batter
HAVING COUNT(ball) >= 100
ORDER BY strike_rate DESC
LIMIT 10;'''
    st.write(run_query(query))
	

with st.expander("**03. - Most sixes hit in Test matches**"):
    query = '''SELECT batter, COUNT(*) AS sixes
FROM test_matches
WHERE runs_batter = 6
GROUP BY batter
ORDER BY sixes DESC
LIMIT 10;'''
    st.write(run_query(query))

with st.expander("**04. Most centuries in ODIs**"):
    query = '''SELECT batter, COUNT(*) AS centuries
FROM (
  SELECT match_id, batter, SUM(runs_batter) AS total_runs
  FROM odi_matches
  GROUP BY match_id, batter
  HAVING total_runs >= 100
)
GROUP BY batter
ORDER BY centuries DESC
LIMIT 10;'''
    st.write(run_query(query))

with st.expander("**05. Most ducks (0 runs) in IPL**"):
    query = '''SELECT batter, COUNT(*) AS ducks
FROM (
  SELECT match_id, batter, SUM(runs_batter) AS total_runs
  FROM t20_matches
  GROUP BY match_id, batter
  HAVING total_runs = 0
)
GROUP BY batter
ORDER BY ducks DESC
LIMIT 10; '''
    st.write(run_query(query))

## Bowling Insights

with st.expander("**06. Leading wicket-takers in T20 matches**"):
    query = '''SELECT bowler, COUNT(*) AS wickets
FROM t20_matches
WHERE wicket_kind IS NOT NULL
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10;'''
    st.write(run_query(query))
	
with st.expander("**07. Best bowling average in ODIs (min 10 wickets)**"):
    query = '''SELECT bowler, ROUND(SUM(runs_total) * 1.0 / COUNT(*), 2) AS bowling_avg
FROM odi_matches
WHERE wicket_kind IS NOT NULL
GROUP BY bowler
HAVING COUNT(*) >= 10
ORDER BY bowling_avg ASC
LIMIT 10;'''
    st.write(run_query(query))

with st.expander("**08. Economy rate of bowlers in IPL (min 60 balls)**"):
    query = '''SELECT bowler, ROUND(SUM(runs_total) * 6.0 / COUNT(ball), 2) AS economy
FROM t20_matches
GROUP BY bowler
HAVING COUNT(ball) >= 60
ORDER BY economy ASC
LIMIT 10;'''
    st.write(run_query(query))

with st.expander("**09. Most dot balls bowled in Test matches**"):
    query = '''SELECT bowler, COUNT(*) AS dot_balls
FROM test_matches
WHERE runs_total = 0
GROUP BY bowler
ORDER BY dot_balls DESC
LIMIT 10; '''
    st.write(run_query(query))

with st.expander("**10. Most maiden overs in ODIs**"):
    query = '''
           SELECT match_id, bowler, COUNT(*) AS maiden_overs
FROM (
  SELECT match_id, bowler, over, SUM(runs_total) AS total_runs
  FROM odi_matches
  GROUP BY match_id, bowler, over
  HAVING total_runs = 0
)
GROUP BY match_id, bowler
ORDER BY maiden_overs DESC
LIMIT 10;  
            '''
    st.write(run_query(query))

## Match & Team Insights
with st.expander("**11. Team with highest win percentage in Test cricket**"):
    query = '''SELECT winner AS team, 
       COUNT(*) * 100.0 / (
         SELECT COUNT(*) FROM test_matches 
         WHERE batting_team = winner
       ) AS win_pct
FROM (
  SELECT DISTINCT match_id, winner
  FROM test_matches
  WHERE winner IS NOT NULL
)
GROUP BY team
ORDER BY win_pct DESC
LIMIT 1;'''
    st.write(run_query(query))

with st.expander("**12. Most matches played by a team across formats**"):
    query = '''
          SELECT batting_team, COUNT(*) AS matches_played
FROM (
  SELECT match_id, batting_team FROM test_matches
  UNION ALL
  SELECT match_id, batting_team FROM odi_matches
  UNION ALL
  SELECT match_id, batting_team FROM t20_matches
)
GROUP BY batting_team
ORDER BY matches_played DESC;
            '''
    st.write(run_query(query))

with st.expander("**13. Most wins by a team in T20**"):
    query = '''
          SELECT winner, COUNT(*) AS wins
FROM (
  SELECT DISTINCT match_id, winner
  FROM t20_matches
  WHERE winner IS NOT NULL
)
GROUP BY winner
ORDER BY wins DESC
LIMIT 10;
            '''
    st.write(run_query(query))

with st.expander("**14. Most tied matches in ODIs**"):
    query = '''
          SELECT COUNT(*) AS tied_matches
FROM (
  SELECT DISTINCT match_id
  FROM odi_matches
  WHERE winner IS NULL AND toss_decision IS NOT NULL
);
            '''
    st.write(run_query(query))

with st.expander("**15. Most common venues for Test matches**"):
    query = '''
          SELECT venue, COUNT(DISTINCT match_id) AS matches
FROM test_matches
GROUP BY venue
ORDER BY matches DESC
LIMIT 10;
            '''
    st.write(run_query(query))

## Performance Trends
with st.expander("**16. Average first innings score in T20**"):
    query = '''
          SELECT ROUND(AVG(total_runs), 2) AS avg_score
FROM (
  SELECT match_id, SUM(runs_total) AS total_runs
  FROM t20_matches
  WHERE inning = 1
  GROUP BY match_id
);
            '''
    st.write(run_query(query))

with st.expander("**17.	Highest scoring ODI matches**"):
    query = '''
          SELECT match_id, SUM(runs_total) AS total_runs
FROM odi_matches
GROUP BY match_id
ORDER BY total_runs DESC
LIMIT 5;
            '''
    st.write(run_query(query))

with st.expander("**18. Most extras conceded in a Test match**"):
    query = '''
          SELECT match_id, SUM(runs_extras) AS total_extras
FROM test_matches
GROUP BY match_id
ORDER BY total_extras DESC
LIMIT 5;
            '''
    st.write(run_query(query))

with st.expander("**19. Top partnerships in IPL (batsman + non_striker)**"):
    query = '''
          SELECT batter, non_striker, SUM(runs_total) AS partnership_runs
FROM t20_matches
GROUP BY batter, non_striker
ORDER BY partnership_runs DESC
LIMIT 10;
            '''
    st.write(run_query(query))

with st.expander("**20.	Players with most player-of-the-match awards in ODIs **"):
    query = '''
          SELECT player_of_match, COUNT(DISTINCT match_id) AS awards
FROM odi_matches
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;
            '''
    st.write(run_query(query))
