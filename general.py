### THIS CLUSTERS DATA AND APPENDS THEIR CLASSIFICATION TO THE dump_cleaned CSV 
# Rescources:
# https://scikit-learn.org/stable/modules/clustering.html

import pandas as pd
from sklearn.cluster import AgglomerativeClustering

# Clustering algorithm
def hierachical_cluster(data, threshold=1):
    cl = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold,
        linkage='ward',
    )
    return cl.fit_predict(data)

# Converts a list of key words into a searchable job
def keys_to_str(keys: list, jobs: (list, pd.Series)) -> str:
    # Find a job that contains all the keys
    for job in jobs:
        good_job = True
        
        for key in keys:
            if key not in job:
                good_job = False
        
        # If the job contains all the keys, find the order and return them
        if good_job:
            # Grab starting index of each word
            placement = {key: job.find(key) for key in keys}
            # Sort words into a list by their index
            words = sorted(placement, key=placement.get)
            # Join all the words with spaces
            return ' '.join(words)
    raise AssertionError(f'No job contained all the keys in the group {keys}, suggesting a bad grouping')

# * Matches the title column with a group numbering and a list of keys that relate to each group number
def cluster(vecs: pd.DataFrame, new_col: str, title_column=None, cluster_threshold=1) -> pd.DataFrame:
    # Result in is an np.ndarray of numerical categories
    groups = hierachical_cluster(vecs, cluster_threshold)
    groups = pd.Series(groups, name=new_col)

    print('Clustering grouped', len(groups), 'jobs into', groups.nunique(), 'groups')
    # Merge the title column so that it has something to merge with
    if isinstance(title_column, pd.Series):
        assert len(groups) == len(title_column), f'vecs must be the same length as the title column, not {len(vecs)}, {len(title_column)}'
        # Reset the index to make sure concatentation works as intended
        title_column.reset_index(inplace=True, drop=True)
        groups = pd.concat([groups, title_column], axis=1)
    else:
        groups = pd.DataFrame(groups)

    return groups