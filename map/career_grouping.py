import pandas as pd
import plotly.express as px
from json import dump
from Passion.map.career_map_compile import cluster_mapping

# * Appends a bunch of different labels depending on the cluster thresholds
def group_careers(cmap='map/career_map.csv', new_file='map/career_groups.csv', title_col='tfidfKey', thresholds=[10, 15, 20, 25, 35]) -> pd.DataFrame:
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

def group_to_graph(labels='map/career_groups.csv', new_file='map/career_groups_graph.json', reverse_cols=True) -> dict:
    if isinstance(labels, str):
        labels = pd.read_csv(labels)

    # Reverse the columns so we can iterate through the rows left to right
    if reverse_cols:
        labels = labels.iloc[:, ::-1]

    # Assumes columns decrease in priority from left to right
    prev_col = None
    graph = dict()
    for col_name in labels:
        column = labels[col_name]

        # Look at each entry in the column
        for i, child in column.items():
            # Make sure there is a previous column
            if not isinstance(prev_col, type(None)):
                parent = prev_col.iloc[i]

                # Add the parent, saying that is a subcategory of the child
                if child not in graph:
                    graph[parent].append(child)
                    # It is now a node in our graph
                    graph[child] = []  
            # Special case for the big boy parents
            else:
                graph[child] = []
        # The previous column is now the column we just iterated over
        prev_col = column
    
    if new_file:
        with open(new_file, 'w') as f:
            dump(graph, f)
    return graph

# * Editing functions
def split_graph_node(graph, node, min_children=5):
    for child in graph[node]:
        queue = [child]
        child_strength = 0

        while (child_strength < min_children and queue):
            second_children = graph[queue[0]]
            queue.extend(second_children)
            queue = queue[1:]
            child_strength += len(second_children)

        if child_strength >= min_children:
            graph[node].remove(child)

def rename_node(graph, old_name, new_name):
    # Change all dependencies
    for node in graph:
        if old_name in graph[node]:
            graph.remove(old_name)
            graph.append(new_name)
    # Rename actual node
    graph[new_name] = graph[old_name]
    del graph[old_name]

def edit_graph(graph, trim_nodes=['manager']):
    for node in trim_nodes:
        split_graph_node(graph, node)

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
    edit_graph(df)
    display_graph(df) # , html_file='map/career_grouping_tree.html'
