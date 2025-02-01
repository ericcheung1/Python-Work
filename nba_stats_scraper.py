from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame
from unidecode import unidecode

def parse_row(row):
    """
    Take data from a th and td tag and return it as a list of strings
    """
    return [str(x.string) for x in row.find_all(('th', 'td'))]

def parse_row2(row):
    """
    Take data from a th, td, and a tag and return it as a list of strings
    """
    return [x.text.strip() for x in row.find_all('td')]


############# Scraping for per game data
response1 = requests.get('https://www.basketball-reference.com/leagues/NBA_2024_per_game.html')
response1.encoding = 'utf-8'
nba_soup = Soup(response1.text)
ns_tables = nba_soup.find_all('table') 
ns_table1_rows = ns_tables[0].find_all('tr')

ns_parsed_rows = [parse_row(row) for row in ns_table1_rows[1:]]

per_game = DataFrame(ns_parsed_rows)
per_game.columns = [str(x.string) for x in ns_table1_rows[0].find_all('th')]
per_game.drop(['Awards', 'Rk'], axis=1, inplace=True)
per_game.drop([735], inplace=True)
per_game['Player'] = per_game['Player'].apply(unidecode)
per_game.head()

############ Scraping for avdanced stats data
response2 = requests.get('https://www.basketball-reference.com/leagues/NBA_2024_advanced.html')
response2.encoding = 'utf-8'
advanced_soup = Soup(response2.text)
ads_tables = advanced_soup.find_all('table') 
ads_table1_rows = ads_tables[0].find_all('tr')

ads_parsed_rows = [parse_row(row) for row in ads_table1_rows[1:]]

advanced_stats = DataFrame(ads_parsed_rows)
advanced_stats.columns = [str(x.string) for x in ads_table1_rows[0].find_all('th')]
advanced_stats.drop(['Awards', 'Rk','G', 'GS', 'MP', 'Pos'], axis=1, inplace=True)
advanced_stats.drop([735], inplace=True)
advanced_stats['Player'] = advanced_stats['Player'].apply(unidecode)
advanced_stats.head()

############ Scraping for salary data
response3 = requests.get('https://hoopshype.com/salaries/players/2023-2024/')

salary_soup = Soup(response3.text)
sal_tables = salary_soup.find_all('table')
ss_table_1 = sal_tables[0] 

header_row = ss_table_1.find('thead').find('tr')
header = [header.text.strip() for header in header_row.find_all('td')]

ss_table_1_rows = ss_table_1.find_all('tr')[1:]
salary_parsed_rows = [parse_row2(row) for row in ss_table_1_rows]

salary = DataFrame(salary_parsed_rows, columns=header)
salary.drop('2023/24(*)', axis=1, inplace=True)
salary.columns = ['Rank','Player', 'Salary']
salary.drop('Rank', axis=1, inplace=True)
salary.head()


########### Scraping for total minutes played data
response4 = requests.get('https://www.basketball-reference.com/leagues/NBA_2024_totals.html')
response4.encoding = 'utf-8'
total_min_soup = Soup(response4.text)
tm_tables = total_min_soup.find_all('table')
tm_table1_row = tm_tables[0].find_all('tr')

tm_parsed_row = [parse_row(row) for row in tm_table1_row[1:]]

total_min_table = DataFrame(tm_parsed_row)
total_min_table.columns = [str(x.string) for x in tm_table1_row[0].find_all('th')]
total_min_table = total_min_table[['Player', 'Age', 'Team', 'MP']]
total_min_table['Player'] = total_min_table['Player'].apply(unidecode)
total_min_table.rename(columns={'MP': 'Total Minutes'}, inplace=True)
total_min_table.head()


########### merging bales
int_tab1 = pd.merge(per_game, advanced_stats, how='left', on=('Player', 'Age', 'Team'))
int_tab1.head()

int_tab2 = pd.merge(int_tab1, salary, how='left', on='Player')
nba_salary_stats_2024 = pd.merge(int_tab2, total_min_table, how='left', on=('Player', 'Age', 'Team'))


########### cleaning data 
nba_salary_stats_2024['Salary'] = nba_salary_stats_2024['Salary'].str.replace(',', '')
nba_salary_stats_2024['Salary'] = nba_salary_stats_2024['Salary'].str.replace('$', '')
nba_salary_stats_2024.replace(to_replace='None', value=0, inplace=True)
nba_salary_stats_2024.fillna(0, inplace=True)
nba_salary_stats_2024.rename(columns={'Player': 'Player Name',
                                      'Pos': 'Position'}, inplace=True)

str_cols = ['Player Name', 'Team', 'Position']
int_cols = ['Age', 'G', 'GS', 'Salary', 'Total Minutes']
float_cols = [x for x in nba_salary_stats_2024.columns 
              if not ((x in str_cols) or (x in int_cols))]
nba_salary_stats_2024[float_cols] = nba_salary_stats_2024[float_cols].astype(float)
nba_salary_stats_2024[int_cols] = nba_salary_stats_2024[int_cols].astype(int)
nba_salary_stats_2024.drop_duplicates(subset=['Player Name', 'Age'], inplace=True)

nba_salary_stats_2024.head()
nba_salary_stats_2024.tail()
