import pandas as pd
from general import CLEAN_DUMP, VITALS
from general import get_dump

def filter_data(amt=1e4): 
    vitals = pd.read_csv(VITALS)['site']

    print('Reading in clickstream data...')
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
    filter_data()