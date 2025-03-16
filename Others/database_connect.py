import numpy as np
import pandas as pd
import sqlite3

data = pd.read_csv('C:/Users/Eric/Documents/python/Python-Work/nba_stats_salary_2024.csv', index_col=0)

player_table = data[['Player Name']].drop_duplicates()
player_table.rename(columns={'Player Name': 'Name'}, inplace=True)

conn = sqlite3.connect('c:/Users/Eric/Documents/SQL/oreilly_getting_started_with_sql-master/nba_db.db')

#player_table.to_sql('players', conn, if_exists='append', index=False)

def get_player_id(player_name):
    query = "SELECT player_id FROM players WHERE name = ?"
    result = conn.execute(query, (player_name,)).fetchone()
    return result[0] if result else None

# Apply the function to map the player_name column to player_id
data['player_id'] = data['Player Name'].apply(get_player_id)
data['season'] = '2023-24'

BasicStats = data.loc[:, ['Age', 'Team', 'Position', 'G', 
                       'GS', 'MP','ORB', 'DRB', 
                       'TRB', 'AST', 'STL', 'BLK', 
                       'TOV', 'PF', 'PTS', 'Salary',
                       'player_id', 'season']]

#BasicStats.to_sql('BasicStats', conn, if_exists='append', index=False)

ShootingStats = data.loc[:, ['FG', 'FGA', 'FG%', '3P', 
                             '3PA', '3P%', '2P', '2PA', 
                             '2P%', 'eFG%','FT', 'FTA', 
                             'FT%', 'player_id', 'season']]

#  FG REAL, FGA REAL,
#     FG_PCT REAL, FG3M REAL,
#     FG3A REAL, FG3_PCT REAL,
#     FG2M REAL, FG2A REAL, 
#     FG2_PCT REAL, eFG_PCT REAL, 
#     FT REAL, FTA REAL,
#     FT_PCT REAL, 

# 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%',
#        'FT', 'FTA', 'FT%',

ShootingStats.rename(columns={'FG%': 'FG_PCT', '3P': 'FG3M',
                      '3PA': 'FG3A', '3P%': 'FG3_PCT',
                      '2P': 'FG2M', '2PA': 'FG2A',
                      '2P%': 'FG2_PCT', 'eFG%': 'eFG_PCT',
                      'FT%': 'FT_PCT'}, inplace=True)

#ShootingStats.to_sql('ShootingStats', conn, if_exists='append', index=False)

    # PER REAL, TS_PCT REAL, FG3PAr REAL, FTr REAL,
    # ORB_PCT REAL, DRB_PCT REAL, TRB_PCT REAL, AST_PCT REAL,
    # STL_PCT REAL, BLK_PCT REAL, TOV_PCT REAL, USG_PCT REAL,
    # OWS REAL, DWS REAL, WS REAL, WSPER48 REAL, 
    # OBPM REAL, DBPM REAL, BPM REAL, VORP REAL,

    # 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
    #    'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48'

AdvancedStats = data.iloc[:, 29:]
AdvancedStats.pop('Salary')
AdvancedStats.rename(columns={'TS%': 'TS_PCT', '3PAr': 'FG3PAr',
                              'ORB%': 'ORB_PCT', 'DRB%': 'DRB_PCT',
                              'TRB%': 'TRB_PCT', 'AST%': 'AST_PCT',
                              'STL%': 'STL_PCT', 'BLK%': 'BLK_PCT',
                              'USG%': 'USG_PCT', 'WS/48': 'WSPER48',
                              'Total Minutes': 'Total_Minutes',
                              'TOV%': 'TOV_PCT'}, inplace=True)

#AdvancedStats.to_sql('AdvancedStats', conn, if_exists='append', index=False)

