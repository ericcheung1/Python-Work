import sqlite3
from player_ids import get_player_ids


def insert_prep(df, db_path):

    df_copy = df.copy()

    df_copy['player_id'] = df_copy['Player'].apply(get_player_ids, db_path=db_path)

    id_col = df_copy.pop('player_id')
    df_copy.insert(0, 'player_id', id_col)
    df_copy.drop(['Player'], axis=1, inplace=True)

    df_columns = df_copy.columns
    
    replace_dict = {'3': '_3', '2': '_2', '%': '_PCT', '/': 'PER'}

    for key, val in replace_dict.items():
        df_columns = [ele.replace(key, val) for ele in df_columns]
        

    df_copy.columns = df_columns

    return df_copy
