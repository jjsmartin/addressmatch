import os
import hashlib
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


def deterministic_row_id(row):
    pieces = [str(row.name)] + [str(v) for v in row.values]
    text = "|".join(pieces)  # delimiter can be anything unambiguous
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def connected_components_to_lookup(components):
    lookup = {}
    for component in components:
        first_id = next(iter(component))  # get the first id in the component
        lookup[first_id] = list(component)  # convert the set to a list
    return lookup
