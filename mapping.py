import pandas as pd
import numpy as np
from tqdm import tqdm

import plotly.express as px
from sklearn.manifold import TSNE

from general import get_clean_dump, CLEAN_DUMP, MATRIX

# Ensures sites are strongest in their own axis
def add_selfs(save=True):
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
    if save:
        df.to_csv(CLEAN_DUMP, sep='\t', index=False)
    return df

# (Positive) Pointwise mutual information --> log(p(a,b) / ( p(a) * p(b) ))
# * Standardizes the data in the matrix so that prevalence of a job doesn't affect things
def pmi_matrix(df: pd.DataFrame, positive=False) -> pd.DataFrame:
    # Convert matrix into probablities
    col_totals = df.sum(axis=0)
    total = col_totals.sum()
    row_totals = df.sum(axis=1)
    expected = np.outer(row_totals, col_totals) / total
    df = df / expected
    # Silence distracting warnings about log(0):
    with np.errstate(divide='ignore'):
        df = np.log(df)
    df[np.isinf(df)] = 0.0  # log(0) = 0
    # Set minimum to 0's
    if positive:
        df[df < 0] = 0.0
    return df

# * Creates the matrix
def get_matrix(df=None):
    if isinstance(df, type(None)):
        df = get_clean_dump()

    rows = df['site'].unique()
    cols = df['ref'].unique()
    mtrx = pd.DataFrame(0, index=rows, columns=cols)

    for i, row in tqdm(df.groupby('site')): # ! THIS TAKES 1 HOUR
        for ref, amt in zip(row['ref'], row['amt']):
            mtrx.loc[i, ref] = amt

    mtrx.to_csv(MATRIX) # ! Just in case error occurs with pmi
    print(mtrx.head())
    mtrx = pmi_matrix(mtrx)
    mtrx.to_csv(MATRIX)

def display_map():
    # Collapse to 2D
    mtrx = pd.read_csv(MATRIX, index_col='Unnamed: 0')
    # Calculate new points
    tsne = TSNE(n_components=2, random_state=0)
    vecs = tsne.fit_transform(mtrx.to_numpy())
    # Replace n-dimensional data with the 2D data
    vecs = pd.DataFrame(vecs)
    cmap = pd.merge(mtrx.index, vecs, left_index=True, right_index=True)
    # Display!
    fig = px.scatter(cmap, 
        x=0, y=1,
        # color=color_col,
        hover_name='index',
        title='Wikipedia Articles, mapped',
    )
    fig.show()

if __name__ == "__main__":
    df = add_selfs(save=False)
    get_matrix(df)