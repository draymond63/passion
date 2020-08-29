import pandas as pd
from json import dump

def compile_prereq_graph(og_file='dump_cleaned.csv', new_file='path/career_path_graph.json', title_key='posTitle'):
    # Data
    df = pd.read_csv(og_file)

    assert title_key in df, f'{og_file} does not contain {title_key}'

    # Filter for useful entries
    df = df.filter(items=['memberUrn', title_key, 'startDate'])

    # Sort values by member, and then by startDate
    df = df.sort_values(['memberUrn', 'startDate'], ascending=False)

    graph = {}
    nRow = df.iloc[0] # Set initial value fo the next row so the cRow will be at 0

    for i in range(len(df) - 1):
        cRow = nRow
        nRow = df.iloc[i + 1]

        title = cRow[title_key]
        # Add node if it is not in the graph
        if title not in graph:
            graph[title] = {}

        # Add the current edge it
        # If the next job is from the same person and they didn't start two jobs at once
        if cRow['memberUrn'] == nRow['memberUrn'] and cRow['startDate'] != nRow['startDate'] and cRow[title_key] != nRow[title_key]:
            preReq = nRow[title_key]
            # If the job is already prerequisite that has been recorded, add 1 the edge's strength
            if preReq in graph[title]:
                graph[title][preReq] += 1
            # If the prerequisite is new for this job, create the edge and give it a weight of 1
            else:
                graph[title][preReq] = 1

    with open(new_file, 'w') as file:
        dump(graph, file)

if __name__ == "__main__":
    compile_prereq_graph()
    compile_prereq_graph(new_file='path/career_path_graph_keys.json', title_key='tfidfKey')