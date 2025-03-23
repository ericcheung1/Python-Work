import scraper2
import cleaner
import pandas as pd
import insert
import player_ids
import sqlite3

url1 = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
pg = scraper2.scrape_page(url1)
pg_cleaned = cleaner.clean_bbref(pg)

url2 = 'https://www.basketball-reference.com/leagues/NBA_2024_advanced.html'
url3 = 'https://hoopshype.com/salaries/players/2023-2024/'

ad = scraper2.scrape_page(url2)
ad_cleaned = cleaner.clean_bbref(ad)

sal = scraper2.scrape_page(url3)
sal_cleaned = cleaner.clean_salary(sal)

merged = cleaner.salary_match(pg_cleaned, sal_cleaned)

insert_prep_merge = insert.insert_prep(merged, 'nba_test.db')
insert_pred_advanced = insert.insert_prep(ad_cleaned, 'nba_test.db')

player_ids.get_player_ids('Kawhi Leonard', db_path='nba_test.db')

# approach 1
cols = merged.columns
old_substring = '%'
new_substring = '_PCT'
new_cols = [s.replace(old_substring, new_substring) for s in cols]

# approach 2
columns = merged.columns
replace_dict = {'3': '_3', '2': '_2', '%': '_PCT'}

for key, val in replace_dict.items():
    columns = [ele.replace(key, val) for ele in columns]

print(columns)

conn = sqlite3.connect('nba_test.db')
cursor = conn.cursor()


cursor.execute('PRAGMA table_info(PerGameBasic)')

per_game_columns = cursor.fetchall()

conn.close()

cursor.execute('PRAGMA table_info(PerGameAdvanced)')
advanced_columns = cursor.fetchall()
conn.close()