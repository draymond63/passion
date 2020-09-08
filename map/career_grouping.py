import pandas as pd
from career_map_compile import cluster_mapping
import plotly.express as px

# * Appends a bunch of different labels depending on the cluster thresholds
def group_careers(cmap='map/career_map.csv', new_file='map/career_groups.csv', title_col='tfidfKey', thresholds=[10, 15, 20, 25, 35, 45]):
    if isinstance(cmap, str):
        cmap = pd.read_csv(cmap)
    print(f'\nCAREER GROUPING WITH {len(thresholds)} THRESHOLDS')
    # We are going to be appending and saving this dataframe
    df = cmap[title_col]

    for threshold in thresholds:
        groups = cluster_mapping(cmap, f'cmap_{threshold}', title_col, threshold)
        df = pd.merge(df, groups, on=title_col)

    print(df.head())

    if new_file:
        df.to_csv(new_file)
    return df

# * Displays the trees for testing
def display_groups(df, html_file=None):
    # Reverse the columns so we can iterate through the rows left to right
    df = df.iloc[:, ::-1]
    labels = []
    parents = []
    # Iterate through each column
    # Assumes each key has a common parent trhoughout all the rows
    prev_col = None
    for col_name in df:
        column = df[col_name]
        # Look at each key and if it is new, add it and it's parent
        for i, key in column.items():
            if key not in labels:
                labels.append(key)
                # If we have a column before it, give it a parent
                if isinstance(prev_col, type(None)):
                    parent = ''
                else:
                    parent = prev_col.iloc[i]
                parents.append(parent)
        # The previous column is now the column we just iterated over
        prev_col = column
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
    display_groups(df) # , html_file='map/career_grouping_tree.html'
