import pandas as pd
from os import path
from tqdm import tqdm
from general import DUMPS, DUMP, CLEAN_DUMP, VITALS, COLUMNS
from general import get_dump, to_tsv_comp

# Group all clickstream files
def compile_data(r=(17, 30)): # ! NOT DONE
    dumps = DUMPS[r[0] : r[1]] if r else DUMPS

    if not path.exists(dumps[0]):
        raise EnvironmentError('Dump files not downloaded. Go to wiki clickstream dumps')

    if path.exists(DUMP):
        print("Using current file")
        df = get_dump()
    else:
        df = pd.read_csv(dumps.pop(0), sep='\t', compression='gzip', names=COLUMNS)

    print(df.head())
    print(df.shape)
    
    for dump in tqdm(dumps):
        tmp = pd.read_csv(dump, sep='\t', compression='gzip', names=['ref', 'site', 'type-2', 'amt-2'])
        print("NEW")
        print(tmp.head())
        print(tmp.shape)

        df = pd.merge(df, tmp, on=['ref', 'site'], how='outer')
        df['amt'] = df['amt'] + df['amt-2'] # ! Makes most of them bad
        df = df.drop(['type-2', 'amt-2'], axis=1)
        print("SUM")
        print(df.head())

    to_tsv_comp(df, DUMP)
    print(df.shape)


def filter_data(amt=1e4): 
    vitals = pd.read_csv(VITALS)['site']

    print('Reading in data...')
    df = get_dump()
    print(df.head())
    print(df.shape)
    # Filter out things that aren't in the vital entries
    df = df[ df['site'].isin(vitals) ]
    df = df[ df['ref' ].isin(vitals) ]
    df = df.dropna()
    print(df.head())
    print(df.shape)
    df.to_csv(CLEAN_DUMP, sep='\t', index=False)

if __name__ == "__main__":
    # compile_data()
    filter_data()