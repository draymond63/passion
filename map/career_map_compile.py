import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from Passion.general import cluster, name_group

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

# space_dim=25, cluster_threshold=20
def create_career_map(og_file='dump_cleaned.csv', new_file='map/career_map.csv', title_col='tfidfKey', num_col='cmapKeyNum', name_col='cmapKey', space_dim=50, cluster_threshold=20) -> pd.DataFrame:
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
        assert num_col and title_col, f'A column name must be given to num_col for clustering to work'
        categories = cluster(vecs=cmap.drop(title_col, axis=1), title_column=cmap[title_col], new_col=num_col, cluster_threshold=cluster_threshold)
        cmap = pd.merge(cmap, categories, how='left', on=title_col)

    # Reset the index cuz it's gonna be weird
    cmap.reset_index(inplace=True, drop=True)

    # * Name the groups
    if name_col:
        grouped_cmap = cmap.groupby(num_col)
        titles = [0] * len(grouped_cmap)
        # Assign a name to each group
        for i, group in grouped_cmap:
            titles[i] = name_group(group[title_col])
        # Add the new titles to the dataset
        titles = pd.Series(titles, name=name_col)
        cmap = pd.merge(cmap, titles, left_on=num_col, right_index=True)
        cmap.sort_index(inplace=True)

    # Save the data if requested
    if new_file:
        cmap.to_csv(new_file, index=False)    
    return cmap

def display_map(cmap: pd.DataFrame, color_col='cmapKey', name_col='tfidfKey', html_file=None):
    # Read in the data if a filename is given
    if isinstance(cmap, str):
        cmap = pd.read_csv(cmap)

    # Slice data to be TSNE'd
    non_data_cols = [color_col, name_col]
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

    # Make sure the colors discontinous and in order
    if isinstance(cmap[color_col].iloc[0], np.int64):
        cmap.sort_values(color_col, ascending=True, inplace=True)
        cmap[color_col] = cmap[color_col].apply(lambda x: str(x))

    fig = px.scatter(cmap, 
        x=0, y=1,
        color=color_col,
        hover_name=name_col
    )
    fig.show()
    if html_file:
        fig.write_html(html_file)

if __name__ == "__main__":
    cmap = create_career_map()
    display_map('map/career_map.csv') # , html_file='map/2DCareerPlot.html'
