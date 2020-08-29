# * Used to convert the dump into a form usable by the neural network
import pandas as pd

def compile_w2v_data(og_file='dump_cleaned.csv', new_file='w2v/w2v_train.json', use_tfidf=True, tfidf_key='tfidfKey'):
    df = pd.read_csv(og_file)

    # Group members by position, but save the groupNum as well if we are using keys
    if use_tfidf: 
        assert tfidf_key in df, f'{tfidf_key} is not in {og_file}'
        train = df.groupby(['jobKey', 'groupNum'])['memberUrn'].apply(list)
    else:
        train = df.groupby(['posTitle'])['memberUrn'].apply(list)

    # Series -> DataFrame & Reset indices
    train = train.to_frame()
    train = train.reset_index()

    # * Group the members into arrays for the jobs
    member_ids = df['memberUrn'].unique().tolist()

    def multiEncodeMembers(urnList):
        l = [0]*len(member_ids)

        for urn in urnList:
            if urn:
                index = member_ids.index(urn)
                l[index] = 1
        return l
    # Multi=encode the members
    train['memberUrn'] = train['memberUrn'].apply(multiEncodeMembers)

    # * Reordering or numbering, depending on incoming data
    if not use_tfidf:
        # Convert the title_key to an integer so that it can be one-hot encoded
        pos_names = df['posTitle'].unique().tolist()
        # Multi=encode the members
        pos_encoded = train['posTitle'].apply(lambda x: pos_names.index(x))
        # Rename is so that it is not still posTitle
        pos_encoded = pos_encoded.rename('posEncoded')
        # Group data together
        train = pd.concat([train, pos_encoded], axis=1)
        train = train.dropna()
        # Reorder columns so it is consistent
        train = train.reindex(columns=['posTitle', 'posEncoded', 'memberUrn'])

    # Rename the columns so the the career map doesn't care about what was added
    train.columns = ['posTitle', 'posEncoded', 'members']

    # Save the file
    train.to_json(new_file)

    print('\nW2V DATA')
    print('# of People:', len(member_ids))
    print('# of Unique Jobs:', train['posEncoded'].nunique())
    print('# of Jobs (Should be the same):', len(train['posEncoded']))
    print(train.head())

if __name__ == "__main__":
    compile_w2v_data()