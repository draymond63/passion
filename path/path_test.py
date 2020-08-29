from path_use import CareerPath
from json import dump
from tqdm import tqdm
import plotly.express as px

# * Displays the trees for testing
def print_tree(tree):
    jobs = list(tree)
    parents = ["" for _ in range(len(jobs))]
    # Copy each prereq
    for job in tree:
        for preReq in tree[job]:
            i = jobs.index(preReq)
            parents[i] = job
    # Display
    fig = px.treemap(
        names = jobs,
        parents = parents
    )
    fig.show()

# * Measures every possible to tree to find anomalies
def tree_stats(graph, level, save_data=False):
    jobs = list(graph.data.keys())
    sizes = {}

    # * Make a tree for each job an determine its size
    for i in tqdm(range(len(jobs))):
        job = jobs[i]
        # Only add graphs where there are children
        if graph.data[job]:
            tree = graph.get_path(job, level)
            sizes[job] = len(tree) 
    
    # Save the list for future use
    if save_data:
        with open(f'./path/testing/path_sizes_{level}.json', 'w') as file:
            dump(sizes, file)
    # Return some stats
    avg = sum(sizes.values()) / len(sizes)
    max_key = max(sizes, key=sizes.get)
    min_key = min(sizes, key=sizes.get)

    return {
        f'{max_key} (max)': sizes[max_key],
        f'{min_key} (min)': sizes[min_key], 
        'avg': round(avg, 4)
    }

graph = CareerPath('./path/career_path_graph_keys.json')
# print(tree_stats(graph, 1))
# print(tree_stats(graph, 2))
# print(tree_stats(graph, 3))
# print(tree_stats(graph, 4))

job = 'nurse'
tree = graph.get_path(job, 1)
print_tree(tree)
tree = graph.get_path(job, 2)
print_tree(tree)
tree = graph.get_path(job, 3)
print_tree(tree)
tree = graph.get_path(job, 4)
print_tree(tree)