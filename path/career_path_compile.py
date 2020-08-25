# Libraries used to train models & manipulate data
import pandas as pd

### Kaggle import: https://github.com/Kaggle/kaggle-api
# kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data
df = pd.read_csv(r'../dump.csv')
# Filter for useful entries 
df = df.filter(items=['memberUrn', 'posTitle', 'startDate'])
# Simplify the member id
df['memberUrn'] = df['memberUrn'].apply(lambda x: int(x.split(':')[-1]))
# Lowercase every job
df['posTitle'] = df['posTitle'].str.lower()

# * Only values that have multiple inputs
rep_times = 3 # Only jubs that appear 3 times or more
df = df[df.groupby('posTitle')['posTitle'].transform('count') >= rep_times]
df = df.drop_duplicates()

# Sort values by member, and then by startDate
df = df.sort_values(['memberUrn', 'startDate'], ascending=False)

graph = {}

nRow = df.iloc[0] # Set initial value fo the next row so the cRow will be at 0

for i in range(len(df) - 1):
    cRow = nRow
    nRow = df.iloc[i + 1]

    title = cRow['posTitle']
    # Add node if it is not in the graph
    if title not in graph:
        graph[title] = {}

    # Add the current edge it
    # If the next job is from the same person and they didn't start two jobs at once
    if cRow['memberUrn'] == nRow['memberUrn'] and cRow['startDate'] != nRow['startDate']:
        preReq = nRow['posTitle']
        # If the job is already prerequisite that has been recorded, add 1 the edge's strength
        if preReq in graph[title]:
            graph[title][preReq] += 1
        # If the prerequisite is new for this job, create the edge and give it a weight of 1
        else:
            graph[title][preReq] = 1

# ? REMOVE ALL GRAPHS OF WEIGHT 1

import json

with open('career_path_graph.json', 'w') as file:
    json.dump(graph, file)