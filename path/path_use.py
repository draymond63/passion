from json import load

class CareerPath():
    def __init__(self, file_name=None, dictionary=None):
        # * Store json as a dictionary
        if file_name:
            with open(file_name, 'r') as json_file:
                self.data = load(json_file)
        elif dictionary:
            self.data = dictionary

        # * Calculate average & max weights of the edges
        self.max_weight = 0 # Occurs at ('senior project manager', 'project manager')
        total_sum = 0
        total_count = 0
        # Iterate through each edge
        for key in self.data:
            node = self.data[key]
            for edge in node:
                total_count += 1
                total_sum += node[edge]
                self.max_weight = max(self.max_weight, node[edge])
        
        self.avg_weight = total_sum / total_count

    def _restrict_jobs(self, job_reqs, tree, min_edge_weight, node_child_limit):
        new_job_reqs = dict()
        # Get rid of jobs we have already seen or not strong enough
        for job in job_reqs:
            # Each job is the title which is the key for the strength of that edge
            job_weight = job_reqs[job]
            if job not in tree and job_weight >= min_edge_weight:
                new_job_reqs[job] = job_weight

        # Get ride of weaker jobs until we reached a limit
        if node_child_limit != None:
            while len(new_job_reqs) > node_child_limit:
                # Delete the smallest element from the dictionary
                del new_job_reqs[min(new_job_reqs)]

        # Return the job titles, not the weights
        return list(new_job_reqs)
        
    # Returns a nested dictionary of all the paths
    def _get_path(self, title, min_edge_weight=1, node_limit=None, node_child_limit=None):
        title = title.lower()
        assert title in self.data, f"Given title {title} is not in the graph"
        # Tree that's going to be the path that is returned
        tree = {}
        # Queue of jobs to be added to the tree
        queue = [title]
        # Keep track of how big the tree is
        node_counter = 0

        while len(queue):
            # Grab the dict of prereqs and srink it to satisfy constraints
            job_reqs = self._restrict_jobs(self.data[queue[0]], tree, min_edge_weight, node_child_limit)

            # Add job_reqs as children to the tree
            tree[queue[0]] = job_reqs
            # Add jobs to the queue
            if not node_limit or node_counter < node_limit:
                queue.extend(job_reqs)
            # If the soft limit has been reached add the prereqs to the tree and end it
            else:
                for job in queue:
                    tree[job] = []
                return tree
            
            # Add the number of nodes that are going to be added to the tree
            node_counter += len(job_reqs)
            # Remove this job from the queue
            queue = queue[1:]

        return tree

    def get_path_capped(self, title, soft_max=10, hard_max=20, hard_min=3, max_child=3):
        title = title.lower()
        min_edge = 0

        tree = self._get_path(title, min_edge, node_child_limit=max_child)

        while len(tree) > soft_max:
            min_edge += 1
            tree = self._get_path(title, min_edge, hard_max, max_child)
        
        # If the job has prereqresuites it should have a tree
        if len(tree) < hard_min and self.data[title] != []:
            tree = self._get_path(title, min_edge-1, hard_max, max_child)
        
        return tree

    def get_path_small(self, title):
        return self.get_path_capped(title, 3, 5)
    def get_path_medium(self, title):
        return self.get_path_capped(title, 5, 10)
    def get_path_big(self, title):
        return self.get_path_capped(title, 10, 20)

    def get_path(self, title, size=1):
        assert size in [1, 2, 3, 4], f'Size request must be 1-4, not {size}'

        if size == 1:
            return self.get_path_small(title)
        if size == 2:
            return self.get_path_medium(title)
        if size == 3:
            return self.get_path_big(title)
        else:
            return self.get_path_capped(title, 20, None, max_child=5)
