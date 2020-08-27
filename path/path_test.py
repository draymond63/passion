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

### DATA
# CHILD = 2
# max: 10 ==> {'customer service representative (max)': 22, 'technical assistant (min)': 2, 'avg': 17.9985}
# HARD MAX
# hard: 10==> {'cashier (max)': 13, 'technical assistant (min)': 2, 'avg': 10.8444} (soft max = 5)
# hard: 5 ==> {'guest speaker (max)': 8, 'technical assistant (min)': 2, 'avg': 6.7050}
# hard: 5 ==> {'guest speaker (max)': 8, 'technical assistant (min)': 2, 'avg': 6.5172} (soft max = 3)
# DEFAULT (CHILD=3, HARD MAX=20, HARD MIN=3)
# max: 10 ==> {'marketing and public relations intern (max)': 23, 'technical assistant (min)': 2, 'avg': 18.8613}
# max: 5  ==> {'marketing and public relations intern (max)': 23, 'technical assistant (min)': 2, 'avg': 18.8192}

def tree_stats(graph, soft_max=10, hard_min=3, hard_max=10, save_data=False):
    jobs = list(graph.data.keys())
    sizes = {}

    # * Make a tree for each job an determine its size
    for i in tqdm(range(len(jobs))):
        job = jobs[i]
        # Only add graphs where there are children
        if graph.data[job]:
            tree = graph.get_path_capped(job, soft_max, hard_min=hard_min, hard_max=hard_max)
            sizes[job] = len(tree) 
    
    # Save the list for future use
    if save_data:
        with open(f'./path/testing/path_sizes_{soft_max}.json', 'w') as file:
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

graph = CareerPath('./path/career_path_graph.json')
# print(tree_stats(graph, 8, hard_max=10))

# tree = graph.get_path('ceo', min_edge_weight=6, node_child_limit=3)
# tree = graph.get_path_capped('senior project manager', 10)
# tree = graph.get_path_capped('product manager', 10)
# tree = graph.get_path_capped('CFO', 10)

tree = graph.get_path('cfo', 1)
print_tree(tree)
tree = graph.get_path('cfo', 2)
print_tree(tree)
tree = graph.get_path('cfo', 3)
print_tree(tree)
tree = graph.get_path('cfo', 4)
print_tree(tree)