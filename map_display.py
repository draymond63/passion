import pandas as pd
import numpy as np
from tqdm import tqdm

import plotly.express as px
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from general import CLEAN_DUMP, W2V_MATRIX, VITALS
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

def get_centroids(m_file=W2V_MATRIX, level='l2'):
    mtrx = pd.read_csv(m_file, index_col='site')
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


def display_map(m_file=W2V_MATRIX, level='site', color='l1'):
    assert color in ('site', 'l1', 'l2', 'l3'), "Color must be l1-3 or 'site'"
    assert color in ('l1', 'l2', 'l3'), "Color must be l1-3"
    # Collapse to 2D
    if isinstance(m_file, str):
        mtrx = pd.read_csv(m_file, index_col='site')
    else:
        mtrx = m_file
    # Calculate new points
    tsne = TSNE(n_components=2, random_state=0, verbose=1)
    vecs = tsne.fit_transform(mtrx.to_numpy())
    # Replace n-dimensional data with the 2D data
    vecs = pd.DataFrame(vecs)
    vecs.index = mtrx.index
    # Add the categorization for color
    if color:
        print(vecs.shape)
        categories = pd.read_csv(VITALS).filter((level, color)).drop_duplicates()
        vecs = pd.merge(vecs, categories, left_index=True, right_on=level, how='inner')
        print(vecs[level].nunique())
        print(vecs.shape)
    # Display!
    fig = px.scatter(vecs, 
        x=0, y=1,
        color=color,
        hover_name=level,
        title='Wikipedia Articles, mapped',
    )
    fig.show()
    fig.write_html(f'storage/wiki/wiki-map({level}-{color}).html')

def display_centroids(level='l2'):
    df = get_centroids(level=level)
    display_map(df, level=level, color='l1')


if __name__ == "__main__":
    # df = add_selfs(save=False)
    # display_centroids()
    display_map()