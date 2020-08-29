# * Used to convert the dump into a form usable by the neural network
import pandas as pd

def compile_w2v_data(og_file='dump_cleaned.csv', new_file='w2v/w2v_train.json', use_keys=True):
    if use_keys: 
        title_key = 'jobKey'
    else:
        title_key = 'posTitle'

    members = pd.read_csv(og_file)

    # Group members by position, but save the groupNum as well
    train = members.groupby([title_key, 'groupNum'])['memberUrn'].apply(list) # 2817 jobs w/ more than 1 member
    # Series -> DataFrame & Reset indices
    train = train.to_frame()
    train = train.reset_index()

    print(train.head())

    # * Group the members into arrays for the jobs
    ids = members['memberUrn'].unique().tolist()

    def multiEncodeMembers(urnList):
        l = [0]*len(ids)

        for urn in urnList:
            if urn:
                index = ids.index(urn)
                l[index] = 1
        return l
    # Multi=encode the members
    train['memberUrn'] = train['memberUrn'].apply(multiEncodeMembers)

    # Save the file
    train.to_json(new_file)

    print('# of People:', len(ids))
    print(train.head())

if __name__ == "__main__":
    compile_w2v_data()