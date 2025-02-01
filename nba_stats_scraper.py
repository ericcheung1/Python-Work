from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame

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

response1 = requests.get('https://www.basketball-reference.com/leagues/NBA_2024_per_game.html')
nba_soup = Soup(response1.text)
ns_tables = nba_soup.find_all('table') 
ns_table1_rows = ns_tables[0].find_all('tr')

ns_parsed_rows = [parse_row(row) for row in ns_table1_rows[1:]]

per_game = DataFrame(ns_parsed_rows)
per_game.columns = [str(x.string) for x in ns_table1_rows[0].find_all('th')]
per_game.drop(['Awards', 'Rk'], axis=1, inplace=True)
per_game.drop([735], inplace=True)
per_game.head()


response2 = requests.get('https://www.basketball-reference.com/leagues/NBA_2024_advanced.html')

advanced_soup = Soup(response2.text)
ads_tables = advanced_soup.find_all('table') 
ads_table1_rows = ads_tables[0].find_all('tr')

ads_parsed_rows = [parse_row(row) for row in ads_table1_rows[1:]]

advanced_stats = DataFrame(ads_parsed_rows)
advanced_stats.columns = [str(x.string) for x in ads_table1_rows[0].find_all('th')]
advanced_stats.drop(['Awards', 'Rk','Team', 'G', 'GS', 'MP', 'Pos'], axis=1, inplace=True)
advanced_stats.drop([735], inplace=True)
advanced_stats.head()

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

salary.head()

nba_stats_2024 = pd.merge(per_game, advanced_stats, how='left', on=('Player', 'Age'))
nba_stats_2024.head()


