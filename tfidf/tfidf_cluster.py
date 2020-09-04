from Passion.general import cluster, keys_to_str
import pandas as pd

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

def combine_misc(df, numCol: str, titleCol: str):
    # Gather the indices of each misc group
    misc_groups = []
    for groupName, groupNum in zip(df[titleCol], df[numCol]):
        if groupName == 'misc' and groupNum not in misc_groups:
            misc_groups.append(groupNum)
    
    print(f'Merging {len(misc_groups)} miscellaneous groups into one')

    # Merge all the misc groups into one
    # Iterate through all useless misc groups, putting the largest groupNums in their place
    for groupNum in misc_groups[1:]:
        # Replace all the old misc category numbers with the main misc number
        df[numCol] = df[numCol].apply(
            lambda num: misc_groups[0] if num == groupNum else num)
        # Move the largest categories number to the one that is now empty
        df[numCol] = df[numCol].apply(
            lambda num: groupNum if num == len(df)-1 else num)

    return df

# * Using clustering to append the cleaned dump with job key
def append_keys(appended_file='dump_cleaned.csv', input_file='tfidf/tfidf_positions.csv', title_col='posTitle', name_col='tfidfKey', num_col='tfidfKeyNum', cluster_threshold=1):
    print('\nDATA WITH TFIDF CLUSTERED GROUPINGS')
    df = pd.read_csv(input_file)
    data = df.drop([title_col], axis=1)
    titles = df[title_col]

    # Add groups to the data
    categories = cluster(data, num_col, titles, cluster_threshold=cluster_threshold)
    new_df = pd.merge(df, categories, on='posTitle')
    grouped_df = new_df.groupby(num_col)
    
    # Name each group
    job_keys = [0] * len(grouped_df)
    for i, group in grouped_df:
        # Gather the data for the cluster
        vecs = group.drop([title_col, num_col], axis=1)
        group_titles = group[title_col]
        # Save the name
        job_keys[i] = name_group(vecs, group_titles)

    job_keys = pd.Series(job_keys, name=name_col)
    categories = pd.merge(categories, job_keys, left_on=num_col, right_index=True)

    # Merging into the dump_cleaned
    dump = pd.read_csv(appended_file)
    # Replace the data if it is already there
    if name_col in dump:
        dump.drop(name_col, axis=1, inplace=True)
    if num_col in dump:
        dump.drop(num_col, axis=1, inplace=True)
    
    # Merge the group numbers on the posTitles first
    dump = pd.merge(dump, categories, on=title_col)
    # Sort the rows to bring it back to where it was before
    dump = dump.sort_values(['memberUrn', 'startDate'], ascending=False)
    # Combine misc groups together
    dump = combine_misc(dump, num_col, name_col)

    # Only append the dump if the data isn't already there
    dump.to_csv(appended_file, index=False)

    print(f'Final number of tfidf groups: {max(dump[num_col])}')
    print(dump.shape)
    print(dump.head())

if __name__ == "__main__":
    append_keys()