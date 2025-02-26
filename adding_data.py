import pandas as pd
import sqlite3

data = pd.read_csv('c:/Users/Eric/Documents/R/R-work-in-progress/nba_2022-23_all_stats_with_salary.csv', index_col=0)

conn = sqlite3.connect('c:/Users/Eric/Documents/SQL/oreilly_getting_started_with_sql-master/nba_db.db')

existing_players = pd.read_sql('SELECT * FROM players', conn)
newplayers = data.loc[:, ['Player Name']].drop_duplicates()
newplayers = newplayers[~newplayers['Player Name'].isin(existing_players['name'])]
newplayers.rename(columns={'Player Name': 'Name'}, inplace=True)

newplayers.to_sql('players', conn, if_exists='append', index=False)

all_players = pd.read_sql('SELECT * FROM players', conn)

data = data.merge(all_players, left_on='Player Name', right_on='name',how='left')

data.rename(columns={'GP': 'G'}, inplace=True)
data['season'] = '2022-23'

BasicStats = data.loc[:, ['Age', 'Team', 'Position', 'G', 
                       'GS', 'MP','ORB', 'DRB', 
                       'TRB', 'AST', 'STL', 'BLK', 
                       'TOV', 'PF', 'PTS', 'Salary',
                       'player_id', 'season']]

# BasicStats.to_sql('BasicStats', conn, if_exists='append', index=False)

ShootingStats = data.loc[:, ['FG', 'FGA', 'FG%', '3P', 
                             '3PA', '3P%', '2P', '2PA', 
                             '2P%', 'eFG%','FT', 'FTA', 
                             'FT%', 'player_id', 'season']]

ShootingStats.rename(columns={'FG%': 'FG_PCT', '3P': 'FG3M',
                      '3PA': 'FG3A', '3P%': 'FG3_PCT',
                      '2P': 'FG2M', '2PA': 'FG2A',
                      '2P%': 'FG2_PCT', 'eFG%': 'eFG_PCT',
                      'FT%': 'FT_PCT'}, inplace=True)

# ShootingStats.to_sql('ShootingStats', conn, if_exists='append', index=False)

data.rename(columns={'TS%': 'TS_PCT', '3PAr': 'FG3PAr',
                              'ORB%': 'ORB_PCT', 'DRB%': 'DRB_PCT',
                              'TRB%': 'TRB_PCT', 'AST%': 'AST_PCT',
                              'STL%': 'STL_PCT', 'BLK%': 'BLK_PCT',
                              'USG%': 'USG_PCT', 'WS/48': 'WSPER48',
                              'Total Minutes': 'Total_Minutes',
                              'TOV%': 'TOV_PCT'}, inplace=True)

AdvancedStats = data.loc[:, ['player_id', 'season', 'PER', 'TS_PCT', 
             'FG3PAr', 'FTr', 'ORB_PCT', 'DRB_PCT', 
             'TRB_PCT', 'AST_PCT', 'STL_PCT', 'BLK_PCT', 
             'TOV_PCT', 'USG_PCT', 'OWS', 'DWS', 'WS', 
             'WSPER48', 'OBPM', 'DBPM', 'BPM', 'VORP', 
             'Total_Minutes']]

# AdvancedStats.to_sql('AdvancedStats', conn, if_exists='append', index=False)