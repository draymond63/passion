### THIS CLUSTERS DATA AND APPENDS THEIR CLASSIFICATION TO THE dump_cleaned CSV 
# Rescources:
# https://scikit-learn.org/stable/modules/clustering.html

import pandas as pd
from sklearn.cluster import AgglomerativeClustering

# * Default Clustering algorithm
def hierachical_cluster(data, threshold=1):
    cl = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold,
        linkage='ward',
    )
    return cl.fit_predict(data)


# * Names the groups based off of the titles
def name_group(grouped_freqs: pd.DataFrame, grouped_titles: pd.Series) -> str:
    assert len(grouped_freqs) == len(grouped_titles), f'Frequencies and titles must have the same number of rows, freqs: {len(grouped_freqs)}, titles: {len(grouped_titles)}'

    # Average together the tfidf columns to find the most common words
    word_freqs = grouped_freqs.mean()
    # Get the mose popular words from the group
    keys = word_freqs.nlargest(2, keep='all')
    # We actually want the indices since that is where the words are
    keys = list(keys.index)

    # Since we are using all, if a word has way too many keys, that means it was only meant to have 1
    if len(keys) > 3: 
        keys = word_freqs.nlargest(1, keep='all')
        keys = list(keys.index)
    # If the keys are still too long, it doesn't belong to any category
    if len(keys) > 2:
        keys = 'misc'
    # Convert list to job title (string)
    else:
        keys = keys_to_str(keys, grouped_titles)
    
    # Append the job_keys
    return keys

# * Converts a list of key words into a searchable job
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

# * Combines all groups in the list into one
def combine_group(df, groups, col: str):
    # Merge all the groups into one
    # Iterate through all useless groups, putting the largest groupNums in their place
    for group in groups[1:]:
        # Replace all the old misc category numbers with the main misc number
        df[col] = df[col].apply(
            lambda x: groups[0] if x == group else x)
        # Move the largest categories number to the one that is now empty
        df[col] = df[col].apply(
            lambda x: group if x == len(df)-1 else x)
    return df

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