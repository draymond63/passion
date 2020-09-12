from Passion.general import combine_group
import pandas as pd

# ! THIS SHOULD BE MINIMIZED AS MUCH AS POSSIBLE

def clean_tfidf_keys(og_file='dump_cleaned.csv', num_col='tfidfKeyNum', name_col='tfidfKey'):
    dump = pd.read_csv(og_file)

    # * Remove useless titles
    remove_keys = ['crew member', 'team member', 'committee member', 'secondee', 'cadet']
    for removal_key in remove_keys:
        dump = dump[dump[name_col] != removal_key]

    merge_keys = [
        ['banker', 'private banker', 'personal banker'],
        ['fellow', 'adjunct research fellow', 'honorary fellow', 'teaching fellow', 'research fellow'],
        ['web developer', 'front end developer'],
        ['researcher', 'visiting researcher', 'student researcher'],
        ['project manager', 'project lead'],
        ['lecturer',  'visiting lecturer', 'adjunct lecturer', 'adjunct professor'],
        ['registered nurse', 'clinical nurse specialist'],
        ['keynote speaker', 'keynote presenter'],
        ['auditor', 'internal auditor', 'external auditor'],
        ['manager', 'group manager'],
        ['software developer', 'software engineer'],
        ['student', 'sessional academic']
    ]
    for group in merge_keys:
        # Gather all the relavent group numbers associated with the titles
        groupNums = []
        for key in group:
            nums = list(dump[dump[name_col] == key][num_col])
            if len(nums):
                assert len(set(nums)) == 1, f'{key} resulted in multiple group numbers, {nums}'
                groupNums.append(nums[0])
            else:
                # The first key is what we want the new group to be called, so we don't care if it's in the data
                if key != group[0]:
                    print(f'{key} is not in the data')

        # Replace all the group names
        dump = combine_group(dump, group, name_col)
        dump = combine_group(dump, groupNums, num_col)

    # * Save the file
    dump.to_csv(og_file, index=False)

if __name__ == "__main__":
    clean_tfidf_keys()