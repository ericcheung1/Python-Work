import pandas as pd
import numpy as np
from unidecode import unidecode


def clean_bbref(df):
    """
    Cleans Per Game and Advanced tables from basketball-reference
    """
    try:
        df_copy = df.copy()
        # initial cleaning step
        df_copy.drop(df_copy.tail(1).index, inplace=True)  # drops league average row
        df_copy.drop(["Rk", "Awards"], axis=1, inplace=True)
        df_copy["Player"] = df_copy["Player"].apply(
            unidecode
        )  # removes accents from names
        df_copy["Player"] = df_copy["Player"].str.strip()
        df_copy["Player"] = (
            df_copy["Player"]
            .str.replace(r"(\.(?!\s*Jr))|\s+(I{1,3}V?|IV|VI{0,3}|IX)\b", "", regex=True)
            .str.strip()
        )
        df_copy.replace("", np.nan, inplace=True)  # replaces blanks cells with NaN

        # check for per game or advanced table, changes column names accordingly
        # due to both tables containing MP header, but different variables
        if sum(df_copy.columns.str.contains("VORP")) > 0:
            numeric_cols = ["Age", "G", "GS", "TMP"]
            df_copy.rename(columns={"MP": "TMP"}, inplace=True)
        else:
            numeric_cols = ["Age", "G", "GS"]

        # string and float column specifications
        string_cols = ["Player", "Team", "Pos", "season"]
        float_cols = [
            x
            for x in df_copy.columns
            if not ((x in string_cols) or (x in numeric_cols))
        ]

        # type declaration, uses pd.to_numeric to handle NaNs amongst floats/integers
        df_copy[string_cols] = df_copy[string_cols].astype(str)
        df_copy[numeric_cols] = (
            df_copy[numeric_cols].apply(pd.to_numeric, errors="coerce").astype("Int64")
        )
        df_copy[float_cols] = (
            df_copy[float_cols].apply(pd.to_numeric, errors="coerce").astype("float64")
        )

        return df_copy

    except KeyError as e:
        print(f"Error: {e}")
        return None


def clean_salary(df):
    """"
    Cleans Salary table from hoophype
    """
    df_copy = df.iloc[:, 1:3].copy() # creates copy of needed rows
    df_copy.columns = ["Player", "Salary"] 
    df_copy["Player"] = df_copy["Player"].apply(unidecode)
    df_copy["Player"] = df_copy["Player"].str.strip()
    df_copy["Salary"] = df_copy["Salary"].str.replace(",", "")
    df_copy["Salary"] = df_copy["Salary"].str.replace("$", "")
    df_copy["Salary"] = df_copy["Salary"].apply(pd.to_numeric, errors="coerce").astype("Int64")

    return df_copy


def salary_match(df1, df2):
    """"
    Merges salary with per game tables then rearranged columns
    """
    merged = pd.merge(df1, df2, how="left", on="Player")
    salary_col = merged.pop('Salary')
    merged.insert(1, 'Salary', salary_col)
    
    return merged
