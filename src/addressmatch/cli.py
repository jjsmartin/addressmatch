import click
import pandas as pd
import networkx as nx

from .normalisation import (
    normalise_names, 
    normalise_addresses, 
    split_address
)
from .helpers import (
    save_all_normalised,
    read_normalised,
    deterministic_row_id,
    connected_components_to_lookup
)
from .deduplication import (
    get_cosine_similarity
)


ABBREVIATIONS = {
    'St': 'Street',
    'Rd': 'Road',
    'Ave': 'Avenue',
    'Dr': 'Drive',
    'Pl': 'Place',
    'Ln': 'Lane',
    'Sq': 'Square',
    'Terr': 'Terrace',
}

@click.group()
def cli():
    pass

@cli.command()
@click.argument("input_csv", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
def clean(input_csv, output_dir):
    """Clean names & addresses."""

    restaurants = pd.read_csv(input_csv)

    # add a unique identifier for each restaurant
    restaurants['id'] = restaurants.apply(deterministic_row_id, axis=1)

    # make sure the id in the first column
    restaurants.insert(0, 'id', restaurants.pop('id'))

    split = split_address(restaurants['address'])  

    restaurants = (
        restaurants
        .assign(
            name = lambda df: normalise_names(df.name),
            address = normalise_addresses(split['address_no_postcode']),
            )
        .join(split['postcode'])
        
    )

    # We'll group by this when doing the deduplication, so we don't have to 
    # compare every pair of restaurants.
    restaurants['outcode'] = restaurants['postcode'].str.split(' ').str[0]

    # replace common abbreviations in the address
    restaurants['address'] = (
        restaurants['address']
        .replace(ABBREVIATIONS, regex=True)
    )

    save_all_normalised(restaurants, output_dir)


@cli.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
@click.argument("group_id")
@click.option("--name-threshold", type=float, default=0.1, show_default=True)
@click.option("--address-threshold", type=float, default=0.1, show_default=True)
def dedupe(input_dir, output_dir, group_id, name_threshold, address_threshold):

    """Find duplicates in cleaned data."""

    group = read_normalised(group_id, input_dir)

    # compare all pairs of restaurant *names* in the group
    name_cosine_sim = get_cosine_similarity(group.name)
    address_cosine_sim = get_cosine_similarity(group.address)

    # create a graph from the cosine similarity matrices
    G = nx.Graph()

    n = group.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if name_cosine_sim[i, j] >= name_threshold and address_cosine_sim[i, j] >= address_threshold:
                G.add_edge(group.iloc[i]['id'], group.iloc[j]['id'])

    connected_components = list(nx.connected_components(G))

    lookup = connected_components_to_lookup(connected_components)

    # create a new group ID column in the group DataFrame
    group['group_id'] = (group['id']
                         .map(lambda x: next((k for k, v in lookup.items() if x in v), x)))
    group.insert(0, 'group_id', group.pop('group_id'))

    group = group.sort_values(by='group_id').reset_index(drop=True)

    group.to_csv(f"{output_dir}/{group_id}.csv", index=False)

if __name__ == "__main__":
    cli()