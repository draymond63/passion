import json

class CareerPath():
    def __init__(self, file_name=None, dictionary=None):
        if file_name:
            with open(file_name, 'r') as json_file:
                self.data = json.load(json_file)
        elif dictionary:
            self.data = dictionary
        
    # Returns a nested dictionary of all the paths
    # ! LIMIT NUMBER OF NODES SHOWN
    def get_path(self, title, min_edge_weight=1, node_limit=None):
        assert title in self.data, f"Given title {title} is not in the graph"
        # Tree that's going to be the path that is returned
        tree = {}
        # Queue of jobs to be added to the tree
        queue = [title]
        # Keep track of how big the tree is
        node_counter = 0

        while len(queue):
            # Grab the dict of prereqs for the next job in queue
            dict_job_reqs = self.data[ queue[0] ]
            new_job_reqs = list()

            # Get rid of jobs we have already seen or not strong enough
            for job in dict_job_reqs:
                # Each job is the title which is the key for the strength of that edge
                job_weight = dict_job_reqs[job]
                if job not in tree and job_weight >= min_edge_weight:
                    new_job_reqs.append(job)

            # Add new_job_reqs as children to the tree
            tree[queue[0]] = new_job_reqs
            # Add jobs to the queue
            if node_counter < node_limit:
                queue.extend(new_job_reqs)
            # If the soft limit has been reached add the prereqs to the tree and end it
            else:
                for job in queue:
                    tree[job] = []
                return tree

            # Add the number of nodes that are going to be added to the tree
            node_counter += len(new_job_reqs)
            # Remove this job from the queue
            queue = queue[1:]


        return tree






