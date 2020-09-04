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
def append_keys(appended_file='dump_cleaned.csv', input_file='tfidf/tfidf_positions.csv', new_col='tfidfKey', cluster_threshold=1):
    print('\nDATA WITH TFIDF CLUSTERED GROUPINGS')
    df = pd.read_csv(input_file)
    data = df.drop(['posTitle'], axis=1)
    titles = df['posTitle']

    # Add groups to the data
    new_col_num = new_col+'Num'
    categories = cluster(data, new_col_num, titles, cluster_threshold=cluster_threshold)
    new_df = pd.merge(df, categories, on='posTitle')
    grouped_df = new_df.groupby(new_col_num)
    
    # Name each group
    job_keys = [0] * len(grouped_df)
    for i, group in grouped_df:
        # Gather the data for the cluster
        vecs = group.drop(['posTitle', new_col_num], axis=1)
        group_titles = group['posTitle']
        # Save the name
        job_keys[i] = name_group(vecs, group_titles)

    job_keys = pd.Series(job_keys, name=new_col)
    categories = categories.join(job_keys)

    # Merging into the dump_cleaned
    dump = pd.read_csv(appended_file)
    # Merge the group numbers on the posTitles first
    dump = pd.merge(dump, categories, on='posTitle')
    # Sort the rows to bring it back to where it was before
    dump = dump.sort_values(['memberUrn', 'startDate'], ascending=False)
    # Combine misc groups together
    dump = combine_misc(dump, new_col_num, new_col)

    # Only append the dump if the data isn't already there
    dump.to_csv(appended_file, index=False)

    print(f'Final number of tfidf groups: {max(dump[new_col_num])}')
    print(dump.shape)
    print(dump.head())

if __name__ == "__main__":
    append_keys()