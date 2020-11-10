
# * The dump compiled from https://dumps.wikimedia.org/other/clickstream/
#                    ref                site      path  amt
# Bathtubs_Over_Broadway  Industrial_musical      link   97
#            other-empty  Industrial_musical  external   88
#       Industrial_music  Industrial_musical      link   67
# Shape: (50990825, 4)
DUMP = 'storage/wiki/clickstream-enwiki-2020-09.tsv.gz' # ? 'storage/wiki/clickstream-combined.tsv.gz'
COLUMNS = ['ref', 'site', 'type', 'amt']

# * Vital repos from https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/4/
#     l3            l2      l1              name              site
# Actors  Entertainers  People     Julie Andrews     Julie_Andrews
# Actors  Entertainers  People     Lauren Bacall     Lauren_Bacall
# Shape: (8935, 5) # ! should have 10043
VITALS = 'storage/wiki/vitals.csv'
VITALS_JSON = 'storage/wiki/vitals.json'

# * Original dump, but only with the data from the vital repos
#                    ref                site      path  amt
# Bathtubs_Over_Broadway  Industrial_musical      link   97
#            other-empty  Industrial_musical  external   88
#       Industrial_music  Industrial_musical      link   67
# Shape: (8935, 4)
CLEAN_DUMP = 'storage/wiki/cleaned_clickstream.tsv'

# * Improved compact matrix -> factorized using w2v instead of PSA and PMI
#                        1         2         3         4  ...        148       149       150    
# site                                                    ...  
# 100_metres     -0.044598  0.119342 -0.049774  0.013482  ...  -0.127239 -0.047054  0.050480    
# James_VI_and_I -0.033750  0.102637 -0.088770  0.022699  ...   0.049431 -0.074568 -0.135170 
# Shape: (8935, 150)   
W2V_MATRIX = 'storage/wiki/w2v-matrix.tsv'
# Test analogies
ANALOGIES = 'storage/wiki/analogies.csv'
# Secrets
SECRETS = 'storage/misc/secret_file.json'

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