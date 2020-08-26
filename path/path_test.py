from path_use import CareerPath
import plotly.express as px

def print_tree(tree):
    jobs = list(tree)
    parents = ["" for _ in range(len(jobs))]

    for job in tree:
        for preReq in tree[job]:
            i = jobs.index(preReq)
            parents[i] = job

    fig = px.treemap(
        names = jobs,
        parents = parents
    )
    fig.show()

graph = CareerPath('./career_path_graph.json')

# graph = CareerPath(dictionary={
#     'A': {'B': 2, 'E': 1},
#     'B': {'D': 3},
#     'C': {},
#     'D': {},
#     'E': {'C': 1}
# })

# tree = graph.get_path('ceo', min_edge_weight=6, node_child_limit=3)
# tree = graph.get_path_capped('senior project manager', 10)
tree = graph.get_path_capped('product manager', 10)

print_tree(tree)
print(tree)
print(len(tree))
