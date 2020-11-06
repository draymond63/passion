import pandas as pd
from time import time
from general import get_clean_dump

def get_matrix():
    df = get_clean_dump()
    rows = df['site'].unique()
    cols = df['ref'].unique()

    matrix = pd.DataFrame(0, index=rows, columns=cols)
    print(matrix.head())



if __name__ == "__main__":
    get_matrix()