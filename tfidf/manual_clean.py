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
        ['fellow', 'visiting fellow', 'adjunct research fellow', 'honorary fellow', 'teaching fellow', 'postdoctoral fellow', 'research fellow'],
        ['web developer', 'front end', 'frontend developer', 'web development', 'web architect'],
        ['researcher', 'visiting reseracher', 'student researcher'],
        ['project manager', 'project lead'],
        ['lecturer', 'lecturer tutor', 'visiting lecturer', 'lecturer excercise', 'adjunct lecturer', 'adjunct professor', 'guest lecturer'],
        ['registered nurse', 'clinical nurse'],
        ['keynote presenter', 'keynote speaker', 'guest speaker'],
        ['auditor', 'internal auditor', 'external auditor'],
        ['manager', 'group manager', 'lead', 'group leader'],
        ['software developer', 'software engineer', 'software engineering', 'software development', 'senior software'],
        ['professor of finance', 'professor of economics'],
        ['project manager', 'project leader'],
        ['student', 'casual academic', 'sessional academic']
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