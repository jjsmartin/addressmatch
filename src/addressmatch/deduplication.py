import pandas as pd
import numpy as np
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