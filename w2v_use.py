import pandas as pd
import numpy as np

class CareerMap():
    def __init__(self, df, jobColumn):
        self.jobCol = df[jobColumn]
        self.w2v = df 
        self.vecs = df.drop([jobColumn], axis=1)

    # Index the dataframe for the series representing the 
    def getPoint(self, index=None, title=None):
        assert index or title, "Index or Title must be given"
        
        if index:
            return pd.Series(self.vecs.iloc[index].values[0])

        if title:
            return pd.Series(self.vecs[ self.jobCol == title ].values[0])

    # Add vectors together
    def addIndices(self, a_index, b_index):
        a = self.getPoint(a_index)
        b = self.getPoint(b_index)
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
        # Compute the Euclidean distance
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
        return average

    # A is to B as C is to __
    def analogy(self, a, b, c, approx=True):
        # Make sure titles exist
        assert np.any(self.jobCol == a), f"{a} is not in the career map"
        assert np.any(self.jobCol == b), f"{b} is not in the career map"
        assert np.any(self.jobCol == c), f"{c} is not in the career map"
        # Replace job titles with indices
        a = self.getPoint(title=a)
        b = self.getPoint(title=b)
        c = self.getPoint(title=c)

        point = b.add(-a)
        point = point.add(c)
        # Find closest point
        if approx:
            point = self.findClosest(point)
            # Return the title
            return point['posTitle']
        
        # Otherwise, just return the point
        return point

    # |u|*|v|*cos = a.b
    def cosSim(self, a, b):
        # Norms
        a_norm = np.linalg.norm(a.values)
        b_norm = np.linalg.norm(b.values)
        # Calculations
        dot_product = a.dot(b)
        calc = dot_product/a_norm/b_norm
        return calc
