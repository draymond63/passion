import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from Passion.general import cluster

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

def create_career_map(og_file='dump_cleaned.csv', new_file='map/career_map.csv', title_col='tfidfKey', new_col='cmapKey', space_dim=25, cluster_threshold=20) -> pd.DataFrame:
    print(f"\nPMI'd {'& Collapsed ' if space_dim else ''}Co-occurence Career Map")
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

    co_occerrence = pd.DataFrame(co_occerrence)
    # Use PMI normalize the data
    cmap = pmi_matrix(co_occerrence)
    # Remove useless rows and columns
    cmap.dropna(how='all', axis=0, inplace=True)
    cmap.dropna(how='all', axis=1, inplace=True)

    # Join the title keys
    job_array = pd.Series(job_array, name=title_col)
    # Drop the index before the merge because the indexing has changed
    cmap.reset_index(inplace=True, drop=True)
    cmap = pd.merge(cmap, job_array, left_index=True, right_index=True)

    # Collapse matrix if requested
    if space_dim:
        # PCA works for higher dimensions than TSNE
        pca = PCA(n_components=space_dim, random_state=0)
        collapsed = pca.fit_transform(cmap.drop(title_col, axis=1))
        # Use the new data as the columns
        collapsed = pd.DataFrame(collapsed)
        cmap = pd.merge(cmap[title_col], collapsed, left_index=True, right_index=True)

    # Add groupings if requested
    if cluster_threshold != None:
        assert new_col and title_col, f'A column name must be given to new_col for clustering to work'
        categories = cluster(vecs=cmap.drop(title_col, axis=1), title_column=cmap[title_col], new_col=new_col, cluster_threshold=cluster_threshold)
        cmap = pd.merge(cmap, categories, how='left', on=title_col)

    # Reset the index cuz it's gonna be weird
    cmap.reset_index(inplace=True, drop=True)

    # * print(np.where(pd.isnull(cmap)))
    
    # Save the data if requested
    if new_file:
        cmap.to_csv(new_file)
    return cmap

def display_map(cmap: pd.DataFrame, num_col='cmapKey', name_col='tfidfKey'):
    # Read in the data if a filename is given
    if isinstance(cmap, str):
        cmap = pd.read_csv(cmap)

    # Slice data to be TSNE'd
    non_data_cols = [num_col, name_col]
    data = cmap.drop(non_data_cols, axis=1)

    # Reducing dimensions
    if len(data.columns) != 2:
        # Calculate new points
        tsne = TSNE(n_components=2, random_state=0)
        vecs = tsne.fit_transform(data)
        # Replace n-dimensional data with the 2D data
        data = pd.DataFrame(vecs)
        cmap = cmap.filter(non_data_cols)
        cmap = pd.merge(cmap, data, left_index=True, right_index=True)

    print(cmap.head())

    fig = px.scatter(cmap, 
        x=0, y=1,
        color=num_col,
        hover_name=name_col
    )
    fig.show()

if __name__ == "__main__":
    cmap = create_career_map()
    display_map(cmap)
