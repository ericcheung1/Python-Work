from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests

def scrape_page(url):
    """"
    Takes a Basketball-Reference or Hoophype URL and scrapes the first table
    """
    # fetching the webpage and encoding
    response = requests.get(url)
    response.encoding = 'uft-8'

    # parsing table
    page_soup = Soup(response.text, 'lxml') # parsing page
    table = page_soup.find_all('table') # parsing all tables
    rows = table[0].find_all('tr') # parsing all rows from first table
    
    # parsing each row
    all_parsed_rows = [] # initialize list for all parsed rows
    for row in rows[1:]: # looping through each row starting from second row
        parsed_row = [] # initialize list for current parsed row
        for cell in row.find_all(['th','td']): # Looping through each cell in row
            parsed_row.append(cell.text.strip()) # Appending each cell to row
        all_parsed_rows.append(parsed_row) # Appending each row to all rows

    # formatting as DataFrame
    output = pd.DataFrame(all_parsed_rows)

    # Handles Headers for bbref vs hoophype
    if 'basketball-reference' in url: 
        print("from bbref")
        header = rows[0] # getting header row
        output.columns = [th.text.strip() for th in header.find_all('th')]

        season_num = page_soup.find('h1').find('span')

        if season_num:
            season_text = season_num.text.strip()
    
        output['season'] = season_text

    else:
        print("from hoophype")
        header = table[0].find('thead').find('tr') # getting header row
        output.columns = [th.text.strip() for th in header.find_all('td')]

    return output