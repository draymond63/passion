
# ! Temporarily missing
DUMPS = [
    'storage/temp/clickstream-enwiki-2017-11.tsv.gz',
    'storage/temp/clickstream-enwiki-2017-12.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-01.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-02.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-03.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-04.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-05.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-06.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-07.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-08.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-09.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-10.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-11.tsv.gz',
    'storage/temp/clickstream-enwiki-2018-12.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-01.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-02.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-03.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-04.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-05.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-06.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-07.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-08.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-09.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-10.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-11.tsv.gz',
    'storage/temp/clickstream-enwiki-2019-12.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-01.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-02.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-03.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-04.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-05.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-06.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-07.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-08.tsv.gz',
    'storage/temp/clickstream-enwiki-2020-09.tsv.gz'
]

# * The dump compiled from https://dumps.wikimedia.org/other/clickstream/
#                    ref                site      path  amt
# Bathtubs_Over_Broadway  Industrial_musical      link   97
#            other-empty  Industrial_musical  external   88
#       Industrial_music  Industrial_musical      link   67
# Unique Sites: 4156721 #!
# Unique Refs:  2006915 #!
# Shape:  (50990825, 4)
DUMP = 'storage/clickstream-combined.tsv.gz'
COLUMNS = ['ref', 'site', 'type', 'amt']

# * Original dump, but only with the most popular sites
#
CLEAN_DUMP = 'storage/cleaned_clickstream.tsv'


# * Vital repos from https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/4/
#     l3            l2      l1              name              site
# Actors  Entertainers  People     Julie Andrews     Julie_Andrews
# Actors  Entertainers  People     Lauren Bacall     Lauren_Bacall
# Shape: (10064, 5) # ! should have 10043, but has 10064 (21 extra rows)
VITALS = 'storage/vitals.csv'
VITALS_JSON = 'storage/vitals.json'

# * Matrix of the clean dump, PMI'd -> initial coordinates
MATRIX = 'storage/clickstream-matrix.tsv'
C_MATRIX = 'storage/matrix-compact.tsv'

# ? Start of general purpose functions
import pandas as pd

def to_tsv_comp(df, name):
    df.to_csv(name, sep='\t', index=False, compression='gzip')

def get_dump():
    return pd.read_csv(DUMP, sep='\t', compression='gzip')
def get_clean_dump():
    return pd.read_csv(CLEAN_DUMP, sep='\t')