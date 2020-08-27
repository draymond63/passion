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
# CHILD = 3
# max: 10 ==> {'marketing and public relations intern (max)': 23, 'technical assistant (min)': 2, 'avg': 18.8613}
# max: 5  ==> {'marketing and public relations intern (max)': 23, 'technical assistant (min)': 2, 'avg': 18.8192}
def tree_stats(graph, soft_max=10, save_data=True):
    jobs = list(graph.data.keys())
    sizes = {}

    # * Make a tree for each job an determine its size
    for i in tqdm(range(len(jobs))):
        job = jobs[i]
        # Only add graphs where there are children
        if graph.data[job] != {}:
            tree = graph.get_path_capped(job, soft_max, hard_min=2)
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

# graph = CareerPath(dictionary={
#     'a': {'b': 1, 'c': 2},
#     'b': {'c': 3},  
#     'c': {}
# })

# tree = graph.get_path('ceo', min_edge_weight=6, node_child_limit=3)
# tree = graph.get_path_capped('senior project manager', 10)
# tree = graph.get_path_capped('product manager', 10)
# tree = graph.get_path_capped('CFO', 10)

# print(tree_stats(graph, 5, save_data=False))

tree = graph.get_path_capped('software engineer')
print_tree(tree)