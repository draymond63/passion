### THIS CLUSTERS DATA AND APPENDS THEIR CLASSIFICATION TO THE dump_cleaned CSV 
# Rescources:
# https://scikit-learn.org/stable/modules/clustering.html

import pandas as pd
from sklearn.cluster import AgglomerativeClustering

# * Clustering algorithm
def hierachical_cluster(data, threshold=1):
    # Clusterer
    cl = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold,
        linkage='ward',
    )
    return cl.fit_predict(data)

# * Converts a list of key words into a searchable job
def keys_to_title(keys, group, exclude=None):
    # Ignore option for the misc category
    if keys == exclude:
        return keys

    # Find a job that contains all the keys
    for job in group['posTitle']:
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


# * Using clustering to append the cleaned dump with job key
def append_dump(dump_file='dump_cleaned.csv', tfidf_file='tfidf/tfidf_positions.csv', cluster_threshold=1):
    # Grab the data
    df = pd.read_csv(tfidf_file)
    vecs = df.drop('posTitle', axis=1)
    # Result in is an np.ndarray of numerical categories
    groups = hierachical_cluster(vecs, cluster_threshold)
    groups = pd.Series(groups, name='groupNum')

    print('Clustering grouped', len(groups), 'jobs into', groups.nunique(), 'groups')

    categories = pd.concat([df, groups], axis=1)
    categories_grouped = categories.groupby('groupNum')
    
    jobKeys = {}
    for groupNum, group in categories_grouped:
        # Average together the tfidf columns to find the most common words
        word_freqs = group.drop(['posTitle', 'groupNum'], axis=1)
        word_freqs = word_freqs.mean()
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
        keys = keys_to_title(keys, group, exclude='misc')

        # Save the keys in a nice dict
        jobKeys[groupNum] = keys

    # * Merging into the dump_cleaned
    dump = pd.read_csv(dump_file)
    # Only append the dump if the data isn't already there
    if 'groupNum' not in dump:
        # Merge the group numbers on the posTitles first
        dump = pd.merge(dump, categories.filter(['posTitle', 'groupNum']), on='posTitle')
        # Merge the job keys on the newly joined group numbers
        jobKeys = pd.Series(jobKeys, name='jobKey')
        dump = pd.merge(dump, jobKeys, left_on='groupNum', right_index=True)
        # Sort the rows to bring it back to where it was before
        dump = dump.sort_values(['memberUrn', 'startDate'], ascending=False)
        # Wewrite the dump to include the group number and job keys
        dump.to_csv('dump_cleaned.csv', index=False)
    
    print('\nDATA WITH CLUSTERED GROUPINGS')
    print(dump.head())


if __name__ == "__main__":
    append_dump()