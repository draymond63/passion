
# * The dump compiled from https://dumps.wikimedia.org/other/clickstream/
#                    ref                site      path  amt
# Bathtubs_Over_Broadway  Industrial_musical      link   97
#            other-empty  Industrial_musical  external   88
#       Industrial_music  Industrial_musical      link   67
# Unique Sites: 4156721 #!
# Unique Refs:  2006915 #!
# Shape:  (50990825, 4)
DUMP = 'storage/wiki/clickstream-enwiki-2020-09.tsv.gz' # ? 'storage/wiki/clickstream-combined.tsv.gz'
COLUMNS = ['ref', 'site', 'type', 'amt']

# * Original dump, but only with the most popular sites
#
CLEAN_DUMP = 'storage/wiki/cleaned_clickstream.tsv'


# * Vital repos from https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/4/
#     l3            l2      l1              name              site
# Actors  Entertainers  People     Julie Andrews     Julie_Andrews
# Actors  Entertainers  People     Lauren Bacall     Lauren_Bacall
# Shape: (10064, 5) # ! should have 10043, but has 10064 (21 extra rows)
VITALS = 'storage/wiki/vitals.csv'
VITALS_JSON = 'storage/wiki/vitals.json'

# * Matrix of the clean dump, PMI'd -> initial coordinates
#              index         0         1         2         3         4         5   ...  7708  7709  7710   
# Phaseolus_vulgaris  7.391831  6.867939  4.586909  4.798324  8.020454  0.000000   ...   0.0   0.0   0.0   
#               Tort  0.000000  0.000000  0.000000  0.000000  0.000000  4.723972   ...   0.0   0.0   0.0
# Shape: (2260, 7711)
MATRIX = 'storage/wiki/clickstream-matrix.tsv'
# Shape: (2260, 250)
C_MATRIX = 'storage/wiki/matrix-compact.tsv'
# Improved compact matrix -> factorized using w2v instead of PSA
W2V_MATRIX = 'storage/wiki/w2v-matrix.tsv'


# * CONSTANTS
SPACE_DIM = 200

# ? Start of general purpose functions
import pandas as pd

def to_tsv_comp(df, name):
    df.to_csv(name, sep='\t', index=False, compression='gzip')

def get_dump():
    return pd.read_csv(DUMP, sep='\t', compression='gzip', names=COLUMNS) # ! names=COLUMNS only when dump is directly downloaded
def get_clean_dump():
    return pd.read_csv(CLEAN_DUMP, sep='\t')