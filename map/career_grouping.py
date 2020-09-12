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

# * JSON graph functions
def create_node(name, p, tp, col_num, col_name):
    return {
        'name': name,
        'parent': p,
        'top_parent': tp,
        'child': [],
        'level': (col_num, col_name),
    }

def group_to_graph(labels='map/career_groups.csv', new_file='map/career_groups_graph.json', reverse_cols=True) -> dict:
    if isinstance(labels, str):
        labels = pd.read_csv(labels)

    # Reverse the columns so we can iterate through the rows left to right
    if reverse_cols:
        labels = labels.iloc[:, ::-1]

    # Assumes columns decrease in priority from left to right
    prev_col = None
    graph = dict()
    for col_num, col_name in enumerate(labels):
        column = labels[col_name]
        # Look at each entry in the column
        for i, child in column.items():
            # Make sure there is a previous column
            if not isinstance(prev_col, type(None)):
                parent = prev_col.iloc[i]

                # Add the child, saying that is a subcategory of the parent
                if child not in graph:
                    # Give the parent a child
                    graph[parent]['child'].append(child)
                    # Keep track of it's top parent for future reference
                    top_parent = labels.iloc[i, 0]
                    # Add the node
                    graph[child] = create_node(child, parent, top_parent, col_num, col_name)
            # Special case for the big boy parents
            else:
                graph[child] = create_node(child, '', '', col_num, col_name)
        # The previous column is now the column we just iterated over
        prev_col = column
    
    if new_file:
        with open(new_file, 'w') as f:
            dump(graph, f)
    return graph

# * Graph editing functions
def find_children(graph, node):
    seen = []
    queue = [node]
    # Find all the nodes children and tell it that it is boss
    while (queue):
        children = graph[queue[0]]['child']
        # Move an the item from the queue
        seen.append(queue[0])
        queue = queue[1:]
        # Add all unseen items to the queue
        for item in children:
            if item not in seen:
                queue.append(item)

    # Return only unique items
    seen_u = []
    for item in seen:
        if item not in seen_u:
            seen_u.append(item)
    return seen_u

def move_node_to_top(graph, node, parent):
    seen = find_children(graph, node)
    # Tell the child's children they have to edit their top parents
    for item in seen:
        graph[item]['top_parent'] = node
    # Edit the actual node since it is now a top level node
    graph[node]['top_parent'] = ''
    graph[node]['parent'] = ''
    graph[node]['level'] = graph[parent]['level']

def split_top_parent(graph, node, min_size):
    assert graph[node]['level'][0] == 0, f'Splitting must only occur at the top level, received {node} at level {graph[node]["level"]}'

    new_children = graph[node]['child'].copy()
    for child in graph[node]['child']:
        # Find the child's children
        seen = find_children(graph, child)
        # Check if it passes the criteria
        if len(seen) >= min_size:
            move_node_to_top(graph, child, node)
            # Remove it from the main node's children
            new_children.remove(child)
    graph[node]['child'] = new_children

def rename_node(graph, old_name, new_name):
    assert old_name in graph, f'{old_name} is not a node in the graph'
    # Change all dependencies
    for node in graph:
        # Rename the child
        if old_name in graph[node]['child']:
            graph[node]['child'].append(new_name)
            graph[node]['child'].remove(old_name)
        # Rename the parents
        if old_name == graph[node]['parent']:
            graph[node]['parent'] = new_name
        if old_name == graph[node]['top_parent']:
            graph[node]['top_parent'] = new_name
    # Rename actual node
    graph[new_name] = graph[old_name]
    del graph[old_name]
    # Rename the attribute of the new child
    graph[new_name]['name'] = new_name

def edit_graph(graph, trim_nodes=['manager', 'gi'], min_size=10):
    for node in trim_nodes:
        split_top_parent(graph, node, min_size)

    rename_node(graph, 'gi', 'misc')

# * Displays the trees for testing
def display_graph(graph, html_file=None):
    labels = []
    parents = []
    # Assumes each key has a common parent throughout all the rows
    for node in graph:
        if node not in labels:
            labels.append(node)
            parents.append(graph[node]['parent'])
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
    graph = group_to_graph(df)
    edit_graph(graph)
    display_graph(graph) # , html_file='map/career_grouping_tree.html'
