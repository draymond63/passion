import pandas as pd
import numpy as np
import random
from Passion.general import W2V_MATRIX, VITALS, COLUMNS

class TopicSuggestion():
    def __init__(self, words=[], exclude=[], basic=False, map_path=W2V_MATRIX, category_path=VITALS):
        self.map = pd.read_csv(map_path, index_col='site')
        self.categories = pd.read_csv(category_path, index_col='site')
        # Remove an articles that aren't basic (if required)
        if basic:
            self.categories = self.categories[~self.categories['l4'].isin(('Basics', 'General'))]
        # Remove any excluded l0 categories
        self.categories = self.categories[~self.categories['l0'].isin(exclude)]
        # Remove any vitals that isn't in the map (e.g missing articles)
        self.categories = self.categories[self.categories.index.isin(self.map.index)]
        self.map = self.map[self.map.index.isin(self.categories.index)]
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
    def recommend_topic(self) -> list:
        types = ['center', 'center', 'rand']
        recommendations = self.center_recommendation(k=2) + self.random_recommendation() # + self.edge_recommendation()
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
    def select_topic(self, selection: str):
        assert selection in self.current_recommendations, "Selection was not in the list recommended"
        idx = self.current_recommendations[selection]
        # ! These values should come from somewhere
        if idx == 'center':
            self.radius /= 1.5
        elif idx == 'edge':
            self.radius *= 1.25
            self.update_position(selection)
        elif idx == 'rand':
            self.update_position(selection)

    # Alternative to move_position
    def update_position(self, selection: str):
        print("POSITION")
        print(self.position.head())
        self.likes.append(selection)
        points = self.get_liked_points()
        points = points if len(points) else self.map
        self.position = points.sum() / len(points)
        print("POSITION")
        print(self.position.head())
        


if __name__ == "__main__":
    user = TopicSuggestion(['Quantum mechanics', 'Computer science', 'Artificial intelligence', 'Human behavior', 'Social work'])
    for _ in range(10):
        r = user.recommend_topic()
        print(r)
        user.select_topic(r[int(input())])