from Passion.general import combine_group
import pandas as pd

def clean_tfidf_keys(og_file='dump_cleaned.csv', num_col='tfidfKeyNum', name_col='tfidfKey'):
    dump = pd.read_csv(og_file)

    # * Remove useless titles
    remove_keys = ['crew member', 'team member', 'committee member', 'secondee', 'cadet']
    for removal_key in remove_keys:
        dump = dump[dump[name_col] != removal_key]

    # * Rename bad titles
    rename_keys = {
        # 'national business': '',
        # 'major accounts': '',
        # 'key account': '',
        # 'public relations': '',
        # 'retail sales': '',
        # 'customer service': '',
        'editor chief': 'chief editor',
        # 'general counsel': '',
        # 'quality assurance': '',
        # 'food beverage': '',
        # 'graduate program': '',
        # 'sessional instructor': '',
        # 'head teacher': '',
        # 'work experience': '',
        # 'head operations': '',
        # 'non executive': '',
        # 'head product': '',
        # 'front end': '',
        # 'student research': '',
        # 'full stack': '',
        # 'analyst': '',
        # 'client executive': '',
        # 'community engagement': '',
        # 'business banking': '',
        # 'marketing communications': '',
        # 'desktop support': '',
        # 'client serices': '',
        # 'social media': '',
        # 'chief executive': '',
        # 'chief officer': '',
        # 'senior technology': '',
        # 'summer internship': '',
        # 'sales support': '',
        # 'national sales': '',
        # 'head strategy': '',
        # 'user experience': '',
        # 'product owner': '',
        # 'officer': '',
        # 'peer tutor': '',
        # 'technical support': '',
        # 'director innovation': '',
        # 'national manager': '',
        # 'summer vacationer': '',
        # 'summer clerk': '',
        # 'professional services': '',
        'professor finance': 'professor of finance',
        # 'design lead': '',
        # 'ux designer': '',
        # 'technical expert': '',
        # 'professional player': '',
        # 'human resources': '',
        # 'full time': '',
        # 'it systems': '',
        # 'hr partner': '',
        # 'team lead': '',
        # 'consultant integration': '',
        # 'visiting scholar': '',
        # 'global account': '',
        # 'director consulting': '',
        # 'senior audit': '',
        # 'service delivery': '',
        # 'process control': '',
        # 'qa analyst': '',
        # 'board directors': '',
        # 'lead ux': '',
        # 'legal counsel': '',
        # 'application support': '',
        # 'head marketing': '',
        # 'internal audit': '',
        # 'strategic sourcing': '',
        # 'software test': '',
        # 'expereience designer': '',
        # 'chair board': '',
        # 'founder managing': '',
        # 'test lead': '',
        # 'post doctoral': '',
        # 'head school': '',
        # 'head digital': '',
        # 'learning development': '',
        # 'master administration': '',
        # 'business systems': '',
        # 'application services': '',
        # 'technical team': '',
        # 'undergraduate work': '',
        # 'crm business': '',
        # 'technical lead': '',
        # 'performance test': '',
        # 'senior software': '',
        # 'business intelligence': '',
        'professor economics': 'professor of economics',
        # 'head risk': '',
        # 'bi consultant': '',
        # 'ux consultant': '',
        'program management': 'program manager',
        # 'online marketing': '',
        # 'sap consultant': '',
        # 'internal communications': '',
        # 'enterprise account': '',
        # 'co ordinator': '',
        # 'agile business': '',
        # 'vp engineering': '',
        # 'chairman board': '',
        # 'honorary associate': '',
        # 'head social': '',
        # 'information mamnagement': '',
        # 'personal brand': '',
        # 'creative ux': '',
        # 'rf planning': '',
        # 'sr business': '',
        # 'creative group': '',
        # 'infromation technologu': '',
        # 'sap project': '',
    }
    dump[name_col] = dump[name_col].apply(lambda x: rename_keys[x] if x in rename_keys else x)

    merge_keys = [
        ['banker', 'private banker', 'personal banker'],
        ['fellow', 'visiting fellow', 'adjunct fellow', 'honorary fellow', 'teaching fellow', 'postdoctoral fellow', 'research fellow'],
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
                print(f'{key} is not in the data')

        # Replace all the group names
        dump = combine_group(dump, group, name_col)
        dump = combine_group(dump, groupNums, num_col)

    # * Save the file
    dump.to_csv(og_file)

if __name__ == "__main__":
    clean_tfidf_keys()