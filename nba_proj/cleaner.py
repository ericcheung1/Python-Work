import pandas as pd
import numpy as np
from unidecode import unidecode

def clean_bbref(df):
    """
    Cleans Per Game and Advanced tables from basketball-reference
    """
    try:

        # initial cleaning step
        df.drop(df.tail(1).index, inplace=True) # drops league average row
        df.drop(['Rk', 'Awards'], axis=1, inplace=True) 
        df['Player'] = df['Player'].apply(unidecode) # removes accents from names
        df.replace('', np.nan, inplace=True) # replaces blanks cells with NaN
        
        # check for per game or advanced table, changes column names accordingly
        # due to both tables containing MP header, but different variables 
        if sum(df.columns.str.contains('VORP')) > 0: # checks for 'VORP' in column names
            numeric_cols = ['Age', 'G', 'GS', 'TMP'] 
            df.rename(columns={'MP': 'TMP'}, inplace=True) 
        else:
            numeric_cols = ['Age', 'G', 'GS'] 

        # string and float column specifications
        string_cols = ['Player', 'Team', 'Pos']
        float_cols = [x for x in df.columns if not ((x in string_cols) or (x in numeric_cols))]

        # type declaration, uses pd.to_numeric to handle NaNs amongst floats/integers
        df[string_cols] = df[string_cols].astype(str)
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').astype('Int64')
        df[float_cols] = df[float_cols].apply(pd.to_numeric, errors='coerce').astype('float64')
            
        return df
    
    except KeyError as e:
        print(f'Error: {e}')
        return None
        
