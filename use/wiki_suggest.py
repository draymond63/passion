import pandas as pd
import numpy as np
import random
from Passion.general import W2V_MATRIX, VITALS, COLUMNS

class UserSuggester():
    def __init__(self, words):
        self.map = pd.read_csv(W2V_MATRIX, index_col='site')
        self.categories = pd.read_csv(VITALS, index_col='site')
        # Add categories to the points so the l1 centroids can be calculated
        df = self.map.join(self.categories)
        self.centers = {}
        self.centers['l1'] = df.groupby('l1').agg(lambda x: sum(x)/len(x))
        self.centers['l2'] = df.groupby('l2').agg(lambda x: sum(x)/len(x))
        self.centers['l3'] = df.groupby('l3').agg(lambda x: sum(x)/len(x))
        # Get beginning user coordinate
        self.likes = self.translate(words)
        self.position = self.get_coord() # Uses self.likes
        self.radius = self.get_radius() # ? Encompass all liked wikis
        self.learning_rate = 10 # ? How to set an initial value 

    def translate(self, words):
        translations = {}
        for word in words:
            for key in self.categories:                    
                if word in self.categories[key]:
                    translations[word] = key
                
            # ! else find similar words !
        return pd.DataFrame(translations, columns=['key'])

    def get_like_points(self):
        print(self.likes)

        site_likes = self.likes[self.likes['key'] == 'site']
        points = self.map.filter(site_likes.index)

        for key in ('l1', 'l2', 'l3'):
            key_likes = self.likes[self.likes['key'] == key]
            key_points = self.centers[key].filter(key_likes.index)
            points.append(key_points)
        return points

    def get_coord(self):
        points = self.get_like_points()
        print(points.head(), points.shape)
        return points.sum() / len(points)

    # Distance from self.position to furtherest point in self.likes
    def get_radius(self):
        points = self.get_like_points()
        dist_2 = np.sum((points - self.position)**2, axis=1) # Calculate distance from all point
        print(dist_2)
        return min(dist_2)
            

    


# Suggest three random topics
# Take in user profile and suggest

if __name__ == "__main__":
    us = UserSuggester(['People', 'Lebron James'])
    # print(us.recommend())

# * SURVEY:
# Tell us what you currently like
# - match words they enter with wikis (high confidence)
# Gather value and confidence of each l1 category
# ? - If low confidence, ask them to explain why ?