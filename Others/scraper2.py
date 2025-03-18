from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame
from unidecode import unidecode

per_game = 'https://www.basketball-reference.com/leagues/NBA_2017_per_game.html'

def scrape_nba_reference(url):
    """"
    Takes a Basketball Reference URL and scrapes the first table
    """
    response = requests.get(url)
    response.encoding = 'uft-8'

    page_soup = Soup(response.text, 'lxml')
    table = page_soup.find_all('table')
    rows = table[0].find_all('tr')
    all_parsed_rows = []

    for row in rows[1:]:
        parsed_row = []
        for cell in row.find_all(['th','td']):
            parsed_row.append(cell.text.strip())
        all_parsed_rows.append(parsed_row)


    table = pd.DataFrame(all_parsed_rows)
    header = rows[0]
    table.columns = [th.text.strip() for th in header.find_all('th')]

    return table

df = scrape_nba_reference(per_game)
print(df)