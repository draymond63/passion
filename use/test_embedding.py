import pandas as pd
import numpy as np
from Passion.general import ANALOGIES



class MapTester():
    def __init__(self, df: pd.DataFrame):
        self.mtrx = df
        self.analogies = pd.read_csv(ANALOGIES)

    def get_point(self, site):
        if isinstance(site, (tuple, list)):
            return [self.get_point(p) for p in site]
        else:
            return self.mtrx.loc[site]

    def get_closest(self, vec):
        dist_2 = np.sum((self.mtrx - vec)**2, axis=1) # Calculate distance from all points
        idx = np.argmin(dist_2) # Grab the minimum index
        point = self.mtrx.iloc[idx] # Grab the vector 
        return point.name # Return the wiki

    # A is to B as C is to <result>
    def analogy(self, a, b, c):
        a, b, c = self.get_point((a, b, c))
        r = b - a + c
        return self.get_closest(r)

    def evaluate(self):
        correct = 0
        for _, row in self.analogies.iterrows():
            a, b, c = row[0:3]
            answer = row['answer']
            guess = self.analogy(a, b, c)
            print(guess, answer)
            if guess == answer:
                correct += 1
        return correct / len(self.analogies)


def evaluate(df: pd.DataFrame) -> float:
    m = MapTester(df)
    return m.evaluate()