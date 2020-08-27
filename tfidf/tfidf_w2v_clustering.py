### THIS CLUSTERS DATA AND APPENDS THEIR CLASSIFICATION TO THE dump_cleaned CSV 
# Rescources:
# https://scikit-learn.org/stable/modules/clustering.html

import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering # KMeans

def tfidf_cluster(num_clusters, vecs=None):
    # Data
    if not vecs:
        vecs = pd.read_csv('./tfidf/tfidf_positions.csv', header=None)
    # Clusterer
    return AgglomerativeClustering(num_clusters).fit_predict(vecs)

if __name__ == "__main__":
    result = tfidf_cluster(50)
    print(result)
    print(type(result))
    