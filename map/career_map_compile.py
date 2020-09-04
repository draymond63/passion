import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from Passion.general import cluster

# (Positive) Pointwise mutual information --> log(p(a,b) / ( p(a) * p(b) ))
# * Standardizes the data in the matrix so that prevalence of a job doesn't affect things
def pmi_matrix(df: pd.DataFrame, positive=False):
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

def create_career_map(og_file='dump_cleaned.csv', new_file='career_map.csv', title_col='tfidfKey', new_col='cmapKey', space_dim=None, do_cluster=True):
    df = pd.read_csv(og_file)

    # * Creating a huge matrix where each row is a job and each column is a coordinate
    # Initially each coordinate is the number of people that had both of those jobs
    job_array = df[title_col].unique()
    job_keys = {key:i for i, key in enumerate(job_array)}
    # Creat the initial 2D Matrix
    init_dim = len(job_keys)
    co_occerrence = np.zeros((init_dim, init_dim))

    # Iterate through each person in the group
    people = df.groupby('memberUrn')
    for _, person in people:
        # Make sure they at least have two different jobs
        if person[title_col].nunique() > 1:
            # Make sure each job is in the cmap
            for job1 in person[title_col]:
                for job2 in person[title_col]:
                    coords = (job_keys[job1], job_keys[job2])
                    co_occerrence[coords] += 1

    # Reorganize data
    co_occerrence = pd.DataFrame(co_occerrence)
    job_array = pd.Series(job_array, name=title_col)

    cmap = pmi_matrix(co_occerrence)
    # Join the title keys
    cmap = cmap.join(job_array)
    print(cmap.head())
    print(cmap.shape)
    # Remove useless rows and columns
    # Row dropping only focuses on columns named 0..~540 (everything but title_col)
    cmap.dropna(how='all', axis=1, inplace=True)    
    cmap.dropna(how='all', subset=[*range(len(cmap))], inplace=True)
    print(cmap.head())
    print(cmap.shape)

    if do_cluster:
        categories = cluster(vecs=cmap.drop(title_col, axis=1), title_column=df[title_col], new_col=new_col, cluster_threshold=25)
        cmap = pd.merge(cmap, categories, on=title_col)
        # print(cmap.head())

    # Collapse matrix if requested
    if space_dim:
        # PCA works for higher dimensions than TSNE
        pca = PCA(n_components=space_dim, random_state=0)
        collapsed = pca.fit_transform(cmap.drop(title_col, axis=1))
        # Use the new data as the columns
        collapsed = pd.DataFrame(collapsed)
        cmap = pd.merge(cmap[title_col], collapsed)

    print(f"\nPMI'd {'& Collapsed ' if space_dim else ''}Co-occurence Career Map")
    print(cmap.shape)
    print(cmap.head())

    # Save the data if requested
    if new_file:
        cmap.to_csv(new_file)
    return cmap

def display_map(cmap, groupNumCol='cmapKey', groupNameCol='tfidfKey'):
    non_data_cols = [groupNumCol, groupNameCol]
    data = cmap.drop(non_data_cols, axis=1)

    # Reducing dimensions
    if len(cmap.columns) != 2:
        tsne = TSNE(n_components=2, random_state=0, verbose=1)
        vecs = tsne.fit_transform(data)
        data = pd.DataFrame(vecs)

    cmap = data.join(cmap.filter(non_data_cols))
    print(cmap.head())

    fig = px.scatter(cmap, 
        x=0, y=1,
        color=groupNumCol,
        hover_name=groupNameCol
    )
    fig.show()

if __name__ == "__main__":
    cmap = create_career_map()
    print(cmap.shape)
    # display_map(cmap)
