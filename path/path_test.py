from path_use import CareerPath

graph = CareerPath('./career_path_graph.json')

# graph = CareerPath(dictionary={
#     'A': {'B': 2, 'E': 1},
#     'B': {'D': 3},
#     'C': {},
#     'D': {},
#     'E': {'C': 1}
# })

treeReqs = graph.get_path('ceo', min_edge_weight=2, node_limit=10)

print(treeReqs)
print(len(treeReqs))
