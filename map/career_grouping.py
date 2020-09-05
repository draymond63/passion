import pandas as pd
from career_map_compile import cluster_mapping
import plotly.express as px

# * Appends a bunch of different labels depending on the cluster thresholds
def group_careers(og_file='map/career_map.csv', new_file='map/career_groups.csv', title_col='tfidfKey', thresholds=[10, 15, 20, 25, 35]):
    cmap = pd.read_csv(og_file)
    print(cmap.head())
    # We are going to be appending and saving this dataframe
    df = cmap[title_col]

    for threshold in thresholds:
        groups = cluster_mapping(cmap, f'cmap_{threshold}', title_col, threshold)
        df = pd.merge(df, groups, on=title_col)

    if new_file:
        df.to_csv(new_file)
    return df

# * Displays the trees for testing
def display_groups(df, html_file=None):
    # Reverse the columns so we can iterate through the rows left to right
    df = df.iloc[:, ::-1]
    print(df.head())
    labels = []
    parents = []

    # Iterate through each row, getting the parents in order
    # Assumes each key has a common parent trhoughout all the rows
    for row in df.itertuples():
        row = row[1:] # Remove the index
        last_key = ''
        # Iterate through the keys, adding them to the labels and their predecessor to the parents
        for key in row:
            if key not in labels:
                labels.append(key)
                parents.append(last_key)
            last_key = key

    # Display
    fig = px.treemap(
        names = labels,
        parents = parents
    )
    fig.show()
    # Optionally save it
    if html_file:
        fig.write_html(html_file)

if __name__ == "__main__":
    df = group_careers()
    display_groups(df)
