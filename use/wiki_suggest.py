import pandas as pd
import random
from Passion.general import W2V_MATRIX, VITALS, COLUMNS

class UserSuggester():
    def __init__(self, survey):
        self.map = pd.read_csv(W2V_MATRIX, index_col='site')
        self.categories = pd.read_csv(VITALS, index_col='site')
        # Knowledge about l1, l2, l3 and site preferences
        # Confidence and value?
        self.user = pd.DataFrame(survey)
        self.user.index.name = 'site'
        # Add categories to the points so the l1 centroids can be calculated
        df = self.map.join(self.categories)
        self.centers = {}
        self.centers['l1'] = df.groupby('l1').agg(lambda x: sum(x)/len(x))
        self.centers['l2'] = df.groupby('l2').agg(lambda x: sum(x)/len(x))
        self.centers['l3'] = df.groupby('l3').agg(lambda x: sum(x)/len(x))

    # Picks three, two leaning towards higher likes, and one unconfident
    def recommend(self):
        # Get 3 random L1 categories
        selected = random.choices(self.user.index, weights=self.user['value'], k=2)
        selected.extend(random.choices(self.user.index, weights=1 / self.user['confidence']))
        return [self.pick_article(s) for s in selected]

    def pick_article(self, category):
        # ! CHANGE TO ONLY NOT ONLY USE L1
        options = self.categories[self.categories['l1'] == category]['name']
        return random.choices(options)[0]

    # User gives feedback after making a recommendation (which one was picked, engagement)
    def feedback(self, wiki):
        pass
    


# Suggest three random topics
# Take in user profile and suggest

if __name__ == "__main__":
    us = UserSuggester({
        'confidence': {
            'People': 0.2,
            'History': 0.5,
            'Geography': 0.1,
            'Arts': 0.5,
            'Philosophy_and_religion': 0.3,
            'Everyday_life': 0.1,
            'Society_and_social_sciences': 0.4,
            'Biology_and_health_sciences': 0.3,
            'Physical_sciences': 0.7,
            'Technology': 0.8,
            'Mathematics': 0.1,
        },
        'value': {
            'People': 0.3,
            'History': 0.2,
            'Geography': 0.9,
            'Arts': 0.2,
            'Philosophy_and_religion': 0.1,
            'Everyday_life': 0.5,
            'Society_and_social_sciences': 0.3,
            'Biology_and_health_sciences': 0.3,
            'Physical_sciences': 0.3,
            'Technology': 0.1,
            'Mathematics': 0.1,
        }
    })
    print(us.recommend())

# * SURVEY:
# Tell us what you currently like
# - match words they enter with wikis (high confidence)
# Gather value and confidence of each l1 category
# ? - If low confidence, ask them to explain why ?