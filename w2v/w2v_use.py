import pandas as pd
import numpy as np

class CareerMap():
    def __init__(self, df, jobColumn):
        self.jobCol = df[jobColumn]
        self.w2v = df 
        self.vecs = df.drop([jobColumn], axis=1)

    # Index the dataframe for the series representing the 
    def getPoint(self, info):
        if isinstance(info, int):
            return self.vecs.iloc[info].squeeze()
        elif isinstance(info, str):
            return self.vecs[self.jobCol == info].squeeze()
        else:
            raise TypeError(f'getPoint requires int or str, not {type(info)}')

    # Returns some of vectors
    def add(self, a, b):
        assert isinstance(a, (int, str)), f"add requires int or str, not {type(a)}, {type(b)}"      
        a = self.getPoint(a)
        b = self.getPoint(b)
        return a.add(b)

    # Take the centroid of a list of points
    def avg(self, i_list):
        vec_list = [0] * len(i_list)

        for i, index in enumerate(i_list):
            vec_list[i] = self.getPoint(index)

        df = pd.concat(vec_list, axis=1)
        return df.mean(axis=1)

    def findClosest(self, node, exclude=None):
        # Exclude points as necessary
        if exclude:
            df = self.vecs.drop(exclude)
        else:
            df = self.vecs
        # Compute the Euclidean distance**2
        dist_vect = np.sum((df - node)**2, axis=1)
        # Grab the lowest vector
        index = dist_vect.idxmin()
        # Return the point with the title
        return self.w2v.iloc[index]

    def combJob(self, titles, exclude=None, approx=True):
        # Grab the indices of all titles fiven
        i_list = self.w2v[ self.jobCol.isin(titles) ].index.values

        # Exclude things if necessary
        if exclude:
            assert isinstance(exclude, list), "Exclusion titles must be in a list"
            e_list = self.w2v[ self.jobCol.isin(exclude) ].index.values
        else:
            e_list = None

        # Average the coordinates corresponding to those indices
        average = self.avg(i_list)
        # Find the closest point to the average
        if approx:
            newPoint = self.findClosest(average, e_list)
            # Return the job title
            return newPoint['posTitle']
        return average # Mainly for debugging

    # A is to B as C is to __
    def analogy(self, a, b, c, approx=True):
        # Make sure titles exist
        assert np.any(self.jobCol == a), f"{a} is not in the career map"
        assert np.any(self.jobCol == b), f"{b} is not in the career map"
        assert np.any(self.jobCol == c), f"{c} is not in the career map"
        # Replace job titles with indices
        a = self.getPoint(a)
        b = self.getPoint(b)
        c = self.getPoint(c)

        point = b.add(-a)
        point = point.add(c)
        # Find closest point
        if approx:
            point = self.findClosest(point)
            # Return the title
            return point['posTitle']
        
        # Otherwise, just return the point
        return point # Mainly fo debugging

    # |u|*|v|*cos = a.b
    def cosSim(self, a, b):
        assert type(a) == type(b), f'Types must be the same, received {type(a)} & {type(b)}'
        # Convert titles to points
        if isinstance(a, (str, int)):
            a = self.getPoint(a)
            b = self.getPoint(b)
        # Norms
        a_norm = np.linalg.norm(a.values)
        b_norm = np.linalg.norm(b.values)
        # Calculations
        dot_product = a.dot(b)
        calc = dot_product/a_norm/b_norm
        return calc