import os
import pandas as pd

def save_normalised(outcode, df, location):
    """
    save a single group to the normalised files
    """
    df.to_csv(f"{location}/{outcode}.csv", index=False)


def save_all_normalised(restaurants, location):
    """
    save all the normalised files, one for each outcode
    """

    for outcode, group in restaurants.groupby('outcode'):
        save_normalised(outcode, group, location)


def read_normalised(outcode, location):
    """
    re-read from the normalised files for a single group
    """
    return pd.read_csv(f"{location}/{outcode}.csv")



def read_all_normalised(location):
    """
    read all the normalised files into a single DataFrame
    """
    dfs = []
    for filename in os.listdir(location):
        if filename.endswith('.csv'):
            outcode = filename.split('.')[0]
            dfs.append(read_normalised(outcode, location))

    return pd.concat(dfs, ignore_index=True)