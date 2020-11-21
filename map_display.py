import pandas as pd
import numpy as np
from tqdm import tqdm

import plotly.express as px
from sklearn.manifold import TSNE

from general import W2V_MATRIX, W2V_2D_MAP, VITALS

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


def display_map(m_file=W2V_MATRIX, level='site', color='l1', save_file=W2V_2D_MAP):
    assert color in ('site', 'l0', 'l1', 'l2', 'l3', 'l4'), "Color must be l0-4 or 'site'"
    assert color in ('l0', 'l1', 'l2', 'l3', 'l4'), "Color must be l0-4"
    # Collapse to 2D
    if isinstance(m_file, str):
        mtrx = pd.read_csv(m_file, index_col='site')
    else:
        mtrx = m_file
    # Calculate collapsed points if need
    if mtrx.shape[1] > 2:
        tsne = TSNE(n_components=2, random_state=0, verbose=1)
        vecs = tsne.fit_transform(mtrx.to_numpy())
        # Replace n-dimensional data with the 2D data
        vecs = pd.DataFrame(vecs)
        vecs.index = mtrx.index
    # Save the file if requested
    if save_file:
        vecs.to_csv(save_file, sep='\t')
        get_app_files()
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
        title=f'Wikipedia Articles ({vecs[level].nunique()} points, {vecs[color].nunique()} categories)',
    )
    fig.show()
    fig.write_html(f'storage/wiki/maps/wiki-map({level}-{color}).html')

def display_centroids(level='l2', color='l1'):
    df = get_centroids(level=level)
    display_map(df, level=level, color=color, save_file=None)

# For https://projector.tensorflow.org/
def get_projector_files():
    df = pd.read_csv(W2V_MATRIX, index_col='site')
    df.to_csv('vecs.tmp.tsv', sep='\t', index=False, header=False)
    df.index.to_series().to_csv('labels.tmp.tsv', sep='\t', index=False, header=False)

def get_app_files():
    df = pd.read_csv(W2V_2D_MAP, sep='\t')
    df.to_csv('vecs.csv', index=False, header=False)
    df.index.to_series().to_csv('sites.csv', index=False, header=False)

if __name__ == "__main__":
    # df = add_selfs(save=False)
    # display_centroids(level='l3', color='l0')
    display_map(color='l0')
    # get_projector_files()
    # get_app_files()