import pandas as pd
import numpy as np
import random
from Passion.general import W2V_MATRIX, VITALS, COLUMNS

class TopicSuggestion():
    def __init__(self, words=[]):
        self.map = pd.read_csv(W2V_MATRIX, index_col='site')
        self.categories = pd.read_csv(VITALS, index_col='site')
        # Remove any vitals that isn't in the map (e.g missing articles)
        self.categories = self.categories[self.categories.index.isin(self.map.index)]
        # Keep track of what the user likes and what the user has been recommended
        self.likes = self.translate(words)
        self.recommended = []
        # Get beginning user coordinate
        points = self.get_liked_points()
        points = points if len(points) else self.map # If the user suggests nothing relevant use the center of the map
        self.position = points.sum() / len(points) # Average like points
        self.radius = max(self.pos_dist(points)) # Encompass all liked wikis
        # Feedbacked data
        self.current_recommendations = {}

    # * HELPER FUNCTIONS
    # Convert words to wikis
    def translate(self, words):
        names = self.categories[self.categories['name'].isin(words)]
        return list(names.index)
    def pos_dist(self, points):
        axis = 0 if isinstance(points, pd.Series) else 1
        return np.sum((points - self.position)**2, axis=axis)
    def get_name(self, site):
        return self.categories.loc[site, 'name']
    def get_site(self, name):
        return self.categories[self.categories['name'] == name].index[0]
    def get_liked_points(self):
        return self.map.filter(self.likes, axis='index')

    # * RECOMMENDATIONS
    # Recommend 3 things
    # - within the radius that isn't liked yet (to change radius)
    # - On the edge of the radius              (to change radius/position)
    # - random                                 (to change position)
    def recommend(self) -> list:
        types = ['center', 'edge', 'rand']
        recommendations = self.center_recommendation() + self.edge_recommendation() + self.random_recommendation()
        self.current_recommendations = {r: t for r,t in zip(recommendations, types)}
        return recommendations

    def center_recommendation(self, k=1) -> list:
        filtered_map = self.map.drop(self.likes + self.recommended)
        dists = self.pos_dist(filtered_map)
        dists = pd.DataFrame(dists, index=filtered_map.index, columns=['v'])
        # Get points closest the center
        sites = dists.nsmallest(k, 'v').index
        self.recommended.extend(sites)
        return [self.get_name(s) for s in sites]

    def edge_recommendation(self, k=1) -> list:
        # Calculate distance from edge of the 200 dimensional circle
        filtered_map = self.map.drop(self.likes + self.recommended)
        dists = abs(self.pos_dist(filtered_map) - self.radius)
        dists = pd.DataFrame(dists, index=filtered_map.index, columns=['v'])
        # Check sites near the edge
        edge_proximity = min(dists['v']) + 0.01
        edge_cases = dists[dists['v'] < edge_proximity]
        while (len(edge_cases) < k):
            edge_proximity *= 1.5
            edge_cases = dists[dists['v'] < edge_proximity]
        # print(f'picked {k} from {len(edge_cases)} options')
        # Sample ensures each choice is unique
        sites = random.sample(list(edge_cases.index), k=k)
        # Keep track of what we have recommended & Return it
        self.recommended.extend(sites)
        return [self.get_name(s) for s in sites]

    def random_recommendation(self, k=1) -> list:
        options = self.categories.drop(self.likes + self.recommended)
        return random.choices(options['name'], k=k)

    # * FEEDBACK
    def select(self, selection: str):
        assert selection in self.current_recommendations, "Selection was not in the list recommended"
        idx = self.current_recommendations[selection]
        # ! These values should come from somewhere
        if idx == 'center':
            self.radius /= 1.5
        elif idx == 'edge':
            self.radius *= 1.25
            self.move_position(selection, ratio=0.25)
        elif idx == 'rand':
            self.move_position(selection, ratio=0.5)

    def move_position(self, name: str, ratio: float):
        site = self.get_site(name)
        point = self.map.loc[site]
        increment = self.pos_dist(point) * ratio
        self.position += increment
        


if __name__ == "__main__":
    user = TopicSuggestion(['LeBron James', 'Basketball', 'National Basketball Association'])
    for _ in range(5):
        r = user.recommend()
        user.select(r[1])
        print(r)