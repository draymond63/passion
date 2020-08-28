### THIS CLUSTERS DATA AND APPENDS THEIR CLASSIFICATION TO THE dump_cleaned CSV 
# Rescources:
# https://scikit-learn.org/stable/modules/clustering.html

import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans 
import matplotlib.pyplot as plt
from tqdm import tqdm

# * Found from graph functions
NUMBER_OF_CLUSTERS = 50

df = pd.read_csv('./tfidf/tfidf_positions.csv')
vecs = df.drop('posTitle', axis=1)

def hierachical_cluster(data, threshold=1):
    # Clusterer
    cl = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold,
        linkage='ward',
        memory='./tfidf/clustering_agglo.tmp'
    )
    return cl.fit_predict(data)

def graph_kmeans(min_k, max_k, jump=1):
    # Iterate through each possible number of clusters
    distortions = []
    for i in tqdm(range(min_k, max_k, jump)):
        km = KMeans(
            n_clusters=i, init='random',
            n_init=10, max_iter=300,
            tol=1e-04, random_state=0
        )
        km.fit_predict(vecs)
        distortions.append(km.inertia_)

    # Save the results in case things go south
    pd.Series(distortions).to_csv('tfidf/inertia.tmp.csv')
    # Plot the results
    plt.plot(range(min_k, max_k, jump), distortions, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()

def append_dump():
    # Result in is an np.ndarray of numerical categories
    groups = hierachical_cluster(vecs)
    groups = pd.Series(groups, name='Category')

    print(len(groups))
    print(groups.nunique())

    categories = pd.concat([df['posTitle'], groups], axis=1)
    categories = categories.sort_values('Category')
    print(categories.head(10))


if __name__ == "__main__":
    # graph_kmeans(10, 500, 10)
    append_dump()

