import pandas as pd
from Passion.general import W2V_MATRIX

class UserSuggester():
    def __init__(self, survey, filepath=W2V_MATRIX):
        self.map = pd.read_csv(filepath)
        # Knowledge about l1, l2, l3 and site preferences
        # Confidence and value?
        self.user = {}

    def update_preferences(self, data):
        pass
    


# Suggest three random topics
# Take in user profile and suggest

if __name__ == "__main__":
    us = UserSuggester({
        'confidence': {
            
        },
        'value': {

        }
    })

# * SURVEY:
# Tell us what you currently like
# - match words they enter with wikis (high confidence)
# Gather value and confidence of each l1 category
# ? - If low confidence, ask them to explain why ?