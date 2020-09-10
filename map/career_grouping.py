import pandas as pd
import plotly.express as px
from json import dump
from Passion.map.career_map_compile import cluster_mapping

# * Appends a bunch of different labels depending on the cluster thresholds
def group_careers(cmap='map/career_map.csv', new_file='map/career_groups.csv', title_col='tfidfKey', thresholds=[10, 15, 20, 25, 35]):
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

def prevent_loop(graph, parent):
    queue = [parent]
    while (len(queue)):
        # Add the nodes children to the queue
        queue.extend(graph[queue[0]])
        # Remove the parent
        queue = queue[1:]
        # If the OG parent is back in the queue, there's a loop
        if parent in queue:
            return True
    return False

def group_to_graph(labels='map/career_groups.csv', new_file='map/career_groups.json'):
    if isinstance(labels, str):
        labels = pd.read_csv(labels)

    # Assumes columns increase in priority from left to right
    prev_col = None
    graph = dict()
    for col_name in labels:
        column = labels[col_name]
        # Look at each entry in the column
        for i, parent in column.items():
            if parent not in graph:
                graph[parent] = []

            # Make sure there is a parent column
            if not isinstance(prev_col, type(None)):
                child = prev_col.iloc[i]
                # Add the child, saying that is a subcategory of the parent
                if parent != child and child not in graph[parent]:
                    graph[parent].append(child)
                    # Make sure no loops are being created
                    if prevent_loop(graph, parent):
                        graph[parent].remove(child)
        # The previous column is now the column we just iterated over
        prev_col = column
    
    if new_file:
        with open(new_file, 'w') as f:
            dump(graph, f)
    return graph


# * Displays the trees for testing
def display_graph(graph, html_file=None):
    labels = []
    parents = []
    # Assumes each key has a common parent throughout all the rows
    for parent in graph:
        for child in graph[parent]:
            if child not in labels:
                labels.append(child)
                parents.append(parent)
    
    for parent in parents:
        if parent not in labels:
            labels.append(parent)
            parents.append('')

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
    df = group_careers(new_file=None)
    df = group_to_graph(df)
    display_graph(df) # , html_file='map/career_grouping_tree.html'
