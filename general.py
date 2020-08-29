### THIS CLUSTERS DATA AND APPENDS THEIR CLASSIFICATION TO THE dump_cleaned CSV 
# Rescources:
# https://scikit-learn.org/stable/modules/clustering.html

import pandas as pd
from sklearn.cluster import AgglomerativeClustering

# * Matches the title column with a group numbering and a list of keys that relate to each group number
def cluster(df, new_col, title_column='posTitle', cluster_threshold=1, do_group_naming=True):
    new_col_num = new_col + 'Num'

    # Clustering algorithm
    def hierachical_cluster(data, threshold=1):
        cl = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=threshold,
            linkage='ward',
        )
        return cl.fit_predict(data)

    # Converts a list of key words into a searchable job
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

    # * Names the groups based off of the titles
    def name_group(grouped_df):
        misc_groups = []
        jobKeys = [0] * len(grouped_df)
        for groupNum, group in grouped_df:
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
        # Append the jobKeys
        return pd.Series(jobKeys, name=new_col)
    


    # Grab the data
    vecs = df.drop(title_column, axis=1)
    # Result in is an np.ndarray of numerical categories
    groups = hierachical_cluster(vecs, cluster_threshold)
    groups = pd.Series(groups, name=new_col_num)

    print('Clustering grouped', len(groups), 'jobs into', groups.nunique(), 'groups')

    categories = pd.concat([df, groups], axis=1)
    categories_grouped = categories.groupby(new_col_num)

    # Append a named column
    if do_group_naming:
        jobKeys = name_group(categories_grouped)
        jobKeys = pd.Series(jobKeys, name=new_col)
        categories = pd.merge(categories, jobKeys, left_on=new_col_num, right_index=True)

    # Remove useless data (e.g. tfidf coordinates)
    categories = categories.filter([title_column, new_col, new_col_num])
    return categories