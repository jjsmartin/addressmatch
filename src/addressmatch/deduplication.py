import pandas as pd
import numpy as np
import networkx as nx   
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_cosine_similarity(series: pd.Series) -> np.ndarray:
    vectorizer = TfidfVectorizer(
        ngram_range=(2, 3),  # use 2-grams and 3-grams
        stop_words='english',  # remove common English stop words
        lowercase=True,  # convert to lowercase
        min_df=1,  # include terms that appear in at least one document
    )
    tfidf_matrix = vectorizer.fit_transform(series)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def add_edges(G:nx.Graph, filepath: str) -> nx.Graph:
    """
    Read manual overrides from a CSV file and add edges to the graph.
    The CSV should have two columns: 'id1' and 'id2'.
    """
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        G.add_edge(row['id1'], row['id2'])

    return G

def remove_edges(G:nx.Graph, filepath: str) -> nx.Graph:
    """
    Read manual overrides from a CSV file and remove edges from the graph.
    The CSV should have two columns: 'id1' and 'id2'.
    """
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        G.remove_edge(row['id1'], row['id2'])

    return G