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

def title_availability_stats(graph):
    # ! Computer Systems Analyst --> system analyst
    # ! Auditing clerk --> law clerk
    # ! Nurse --> Registered Nurse
    top_jobs = [
        'Truck Driver', 'Registered Nurse', 'Retail Worker', 'Retail Salesperson', 
        'Software Developer', 'Customer Service Representative', 
        'Marketing Manager', 'Computer User Support Specialist', 'Computer Systems Analyst', 
        'Systems Administrator', 'Web Developer', 'Management Analyst', 
        'Medical and Health Services Manager', 'Accountant', 'Project Manager', 
        'Sales Manager', 'Industrial Engineer', 'Executive Secretary', 
        'Sales Representative', 'Maintenance Worker', 'Social Assistant', 
        'Nursing Assistant', 'Vocational Nurse', 'Operations Manager', 
        'Auditing Clerk', 'Financial Manager', 'Insurance Sales Agent', 
        'Critical Care Nurse', 'Cashier', 'Computer Systems Engineer', 
        'Marketing Specialist', 'Physical Therapist', 'Medical Assistant', 
        'Quality Assurance', 'Information Security Analyst', 'Medical Secretary', 
        'Security Guard', 'Family Practitioner'
    ]
    available = 0
    unavailable = []

    for job in top_jobs:
        if graph.find_title(job):
            available +=1
        else:
            unavailable.append(job)

    percentage = round(available/len(top_jobs)*100, 2)
    print(percentage, '% of top 50 jobs available')
    print('Unavailable Jobs')
    print(unavailable)

graph = CareerPath('path/career_path_graph_keys.json')
# title_availability_stats(graph)
# print(tree_stats(graph, 1))
# print(tree_stats(graph, 2))
# print(tree_stats(graph, 3))
# print(tree_stats(graph, 4))

job = 'Engineer'
tree = graph.get_path(job, 1)
print_tree(tree)
tree = graph.get_path(job, 2)
print_tree(tree)
tree = graph.get_path(job, 3)
print_tree(tree)
tree = graph.get_path(job, 4)
print_tree(tree)