from Passion.general import cluster
import pandas as pd

# * Using clustering to append the cleaned dump with job key
def append_keys(appended_file='dump_cleaned.csv', input_file='w2v/pos_w2v_matrix.json', new_col='w2vKey', cluster_threshold=1):
    print('\nDATA WITH W2V CLUSTERED GROUPINGS')
    df = pd.read_json(input_file)
    categories = cluster(df, new_col, cluster_threshold=cluster_threshold, do_group_naming=False)

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

    # Quickly test the amounnt of people who have more than one job in the same group
    people = dump.groupby('memberUrn')
    success = 0
    total = 0
    for _, person in people:
        person = person.drop_duplicates('tfidfKey')
        if len(person['w2vKeyNum']) != 1:
            total += 1
        if len(person['w2vKeyNum']) != person['w2vKeyNum'].nunique():
            success += 1

    print('People who have multiple unique jobs in the same w2v group:')
    print(success, '/', total, '=', round(success/total, 3)*100, '%') # Averages between 1-10 Depending on the run


if __name__ == "__main__":
    append_keys()
    