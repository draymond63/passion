from path_use import CareerPath
from json import dump
from tqdm import tqdm
import plotly.express as px

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

def tree_stats(graph, soft_max=10):
    jobs = list(graph.data.keys())
    sizes = {}

    # * Make a tree for each job an determine its size
    for i in tqdm(range(len(jobs))):
        job = jobs[i]
        # Only add graphs where there are children
        if graph.data[job] != []:
            tree = graph.get_path_capped(job, soft_max)
            sizes[job] = len(tree) 
    
    # Save the list for future use
    with open(f'./testing/path_sizes_{soft_max}.json', 'w') as file:
        dump(sizes, file)
    # Return some stats
    avg = sum(sizes.values()) / len(sizes)

    return {
        max(sizes): sizes[max(sizes)], 
        min(sizes): sizes[min(sizes)], 
        'avg': avg
    }

graph = CareerPath('./career_path_graph.json')

# graph = CareerPath(dictionary={
#     'a': {'b': 1, 'c': 2},
#     'b': {'c': 3},  
#     'c': {}
# })

# tree = graph.get_path('ceo', min_edge_weight=6, node_child_limit=3)
# tree = graph.get_path_capped('senior project manager', 10)
# tree = graph.get_path_capped('product manager', 10)
# tree = graph.get_path_capped('CFO', 10)

print(tree_stats(graph))

