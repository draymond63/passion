from Passion.general import cluster
import pandas as pd

# * Using clustering to append the cleaned dump with job key
def append_keys(appended_file='dump_cleaned.csv', input_file='tfidf/tfidf_positions.csv', new_col='tfidfKey', cluster_threshold=1):
    print('\nDATA WITH TFIDF CLUSTERED GROUPINGS')
    df = pd.read_csv(input_file)
    categories = cluster(df, new_col, cluster_threshold=cluster_threshold)

    # * Merging into the dump_cleaned
    dump = pd.read_csv(appended_file)
    # Only append the dump if the data isn't already there
    if new_col not in dump:
        # Merge the group numbers on the posTitles first
        dump = pd.merge(dump, categories, on='posTitle')
        # Sort the rows to bring it back to where it was before
        dump = dump.sort_values(['memberUrn', 'startDate'], ascending=False)
        # Wewrite the dump to include the group number and job keys
        dump.to_csv(appended_file, index=False)
    
    print(dump.head())


if __name__ == "__main__":
    append_jobkeys()