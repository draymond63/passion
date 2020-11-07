import pandas as pd
from tqdm import tqdm
from general import get_clean_dump, CLEAN_DUMP

# Ensures sites are strongest in their own axis
def add_selfs():
    df = get_clean_dump()
    print(df.shape)
    selfs = {
        'site': [],
        'ref': [],
        'type': [],
        'amt': []
    }
    for i, row in df.groupby('site')['amt']:
        selfs['site'].append(i)
        selfs['ref'].append(i)
        selfs['type'].append('self')
        selfs['amt'] = row.sum()
    selfs = pd.DataFrame(selfs)
    df = df.append(selfs, ignore_index=True)
    print(df.shape)
    df.to_csv(CLEAN_DUMP, sep='\t', index=False)

def get_matrix():
    df = get_clean_dump()

    rows = df['site'].unique()
    cols = df['ref'].unique()
    matrix = pd.DataFrame(0, index=rows, columns=cols)

    for i, row in tqdm(df.groupby('site')): # ! THIS TAKES 5 HOURS
        for ref, amt in zip(row['ref'], row['amt']):
            matrix.loc[i, ref] = amt

    print(matrix.head())




if __name__ == "__main__":
    # add_selfs()
    get_matrix()