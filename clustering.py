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
def keys_to_title(keys, group):
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

# * Matches the title column with a group numbering and a list of keys that relate to each group number
def cluster(og_file, new_col, title_column='posTitle', cluster_threshold=1):
    new_col_num = new_col + 'Num'
    # Grab the data
    df = pd.read_csv(og_file)
    vecs = df.drop(title_column, axis=1)
    # Result in is an np.ndarray of numerical categories
    groups = hierachical_cluster(vecs, cluster_threshold)
    groups = pd.Series(groups, name=new_col_num)

    print('\nDATA WITH CLUSTERED GROUPINGS')
    print('Clustering grouped', len(groups), 'jobs into', groups.nunique(), 'groups')

    categories = pd.concat([df, groups], axis=1)
    categories_grouped = categories.groupby(new_col_num)
    
    misc_groups = []
    jobKeys = [0] * len(categories_grouped)
    for groupNum, group in categories_grouped:
        # Average together the tfidf columns to find the most common words
        word_freqs = group.drop([title_column, new_col_num], axis=1)
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
            misc_groups.append(groupNum)

        # Convert list to job title (string)
        if keys != 'misc':
            keys = keys_to_title(keys, group)

        # Save the keys in a nice list
        jobKeys[groupNum] = keys

    # * Merge all the misc groups into one
    # Iterate through all useless misc groups, putting the largest groupNums in their place
    for groupNum in misc_groups[1:]:
        # Replace the numbers in the df with the misc group we are keeping
        categories[new_col_num] = categories[new_col_num].apply(
            lambda num: misc_groups[0] if num == groupNum else num)
        # Replace the numbers in the df to switch over the new group
        categories[new_col_num] = categories[new_col_num].apply(
            lambda num: groupNum if num == len(jobKeys)-1 else num)

        # Reassign the group number for when the keys are added
        jobKeys[groupNum] = jobKeys[-1]
        # Pop off the last group since it has been reassigned
        del jobKeys[-1]

    # Remove useless data (e.g. tfidf coordinates)
    categories = categories.filter([title_column, new_col_num])
    # Append the jobKeys
    jobKeys = pd.Series(jobKeys, name=new_col)
    categories = pd.merge(categories, jobKeys, left_on=new_col_num, right_index=True)

    return categories


# * Using clustering to append the cleaned dump with job key
def append_jobkeys(dump_file='dump_cleaned.csv', tfidf_file='tfidf/tfidf_positions.csv', new_col='tfidfKey', cluster_threshold=1):
    categories = cluster(tfidf_file, new_col, cluster_threshold=cluster_threshold)

    # * Merging into the dump_cleaned
    dump = pd.read_csv(dump_file)
    # Only append the dump if the data isn't already there
    if 'groupNum' not in dump:
        # Merge the group numbers on the posTitles first
        dump = pd.merge(dump, categories, on='posTitle')
        # Sort the rows to bring it back to where it was before
        dump = dump.sort_values(['memberUrn', 'startDate'], ascending=False)
        # Wewrite the dump to include the group number and job keys
        dump.to_csv('dump_cleaned.csv', index=False)
    
    print(dump.head())


if __name__ == "__main__":
    append_jobkeys()