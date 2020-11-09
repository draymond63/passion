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
        points = self.get_like_points()
        self.position = points.sum() / len(points) # Average like points
        self.radius = max(np.sum((points - self.position)**2, axis=1)) # Encompass all liked wikis
        self.learning_rate = self.radius * 2 # ? How to set an initial value ?

    # Convert words to wikis
    def translate(self, words):
        # Index by name so we can use the filter function (and the 'like' paramater)
        name_categories = self.categories.reset_index('site')
        name_categories = name_categories.set_index('name')
        # Get the site corresponding to each word
        translations = []
        for word in words:
            sites = name_categories.filter(like=word, axis='index')
            translations.extend(sites['site'])
        return translations

    def get_like_points(self):
        return self.map.filter(self.likes, axis='index')
    
    # Recommend 3 things
    # - within the radius that isn't liked yet (to change positon/learning-rate)
    # - outside the radius                     (to change radius)
    # - random                                 (to change position)
    def recommend(self):
        pass
            

    


# Suggest three random topics
# Take in user profile and suggest

if __name__ == "__main__":
    us = UserSuggester(['LeBron James', 'Basketball', 'National Basketball Association'])
    print(us.recommend())

# * SURVEY:
# Tell us what you currently like
# - match words they enter with wikis (high confidence)
# Gather value and confidence of each l1 category
# ? - If low confidence, ask them to explain why ?