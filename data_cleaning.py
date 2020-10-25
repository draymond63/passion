import pandas as pd
from general import DUMP, POP_DUMP, COLUMNS

def get_popularity():
    print('Reading in data...')
    df = pd.read_csv(DUMP, sep='\t', names=COLUMNS) # compression='gzip'
    df = df.filter(['site', 'amt'], axis=1)
    print('Data read')

    pop = df.groupby('site')['amt'].apply(sum)
    print(pop.head())
    print(pop.shape)
    pop.to_csv(POP_DUMP, sep='\t')


if __name__ == "__main__":
    get_popularity()