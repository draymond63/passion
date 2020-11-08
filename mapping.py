import pandas as pd
import numpy as np
from tqdm import tqdm

import plotly.express as px
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from general import CLEAN_DUMP, MATRIX, C_MATRIX, VITALS
from general import get_clean_dump

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

def shrink_matrix_dim(dim=250):
    mtrx = pd.read_csv(MATRIX, index_col='Unnamed: 0')
    # PCA works for higher dimensions than TSNE
    pca = PCA(n_components=dim, random_state=0)
    cmtrx = pca.fit_transform(mtrx.to_numpy())
    # Use the new data as the columns
    cmtrx = pd.DataFrame(cmtrx)
    cmtrx.index = mtrx.index
    cmtrx.to_csv(C_MATRIX)

def get_centroids(m_file=C_MATRIX, level='l2'):
    mtrx = pd.read_csv(m_file, index_col='Unnamed: 0')
    categories = pd.read_csv(VITALS).filter(['site', level])
    df = pd.merge(mtrx, categories, left_index=True, right_on='site')
    df = df.drop('site', axis=1)

    data = {}
    for category, points in df.groupby(level):
        points = points.drop(level, axis=1)
        count = points.shape[0]
        totals = points.sum()
        center = totals / count # Average coordinates
        data[category] = center.to_list()

    return pd.DataFrame.from_dict(data, orient='index')


def display_map(m_file=C_MATRIX, level='site', color='l2'):
    assert color in ('site', 'l1', 'l2', 'l3'), "Color must be l1-3 or 'site'"
    assert color in ('l1', 'l2', 'l3'), "Color must be l1-3"
    # Collapse to 2D
    if isinstance(m_file, str):
        mtrx = pd.read_csv(m_file, index_col='Unnamed: 0')
    else:
        mtrx = m_file
    # Calculate new points
    tsne = TSNE(n_components=2, random_state=0) # , verbose=1
    vecs = tsne.fit_transform(mtrx.to_numpy())
    # Replace n-dimensional data with the 2D data
    vecs = pd.DataFrame(vecs)
    vecs.index = mtrx.index
    # Add the categorization for color
    if color:
        print(vecs.shape)
        categories = pd.read_csv(VITALS).filter((level, color)).drop_duplicates()
        vecs = pd.merge(vecs, categories, left_index=True, right_on=level, how='inner')
        print(len(mtrx.index))
        print(vecs[level].nunique())
        print(vecs.shape)
    # Display!
    fig = px.scatter(vecs, 
        x=0, y=1,
        color=color,
        hover_name=level,
        title='Wikipedia Articles, mapped',
    )
    # fig.show()
    fig.write_html('storage/wiki_map.html')

def display_centroids():
    df = get_centroids(level='l3')
    display_map(df, level='l3', color='l1')


if __name__ == "__main__":
    # df = add_selfs(save=False)
    # get_matrix(df)
    # shrink_matrix_dim()
    # display_centroids()
    print(get_clean_dump().head())
