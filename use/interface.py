from method_suggest import MethodSuggestion

# MethodSuggestion imports from TopicSuggestion
class Suggestion(MethodSuggestion):
    # def __init__(self):
    #     super(Suggestion, self).__init__()
    def suggest(self):
        recommendations = self.recommend_topic()
        print(recommendations)
        selection = recommendations[int(input())]
        self.select_topic(selection) # Update topic map
        
        responses = [self.methods[key](selection) for key in self.methods]
        print(responses)
        return responses




Suggestion(methods=['wiki'], words=['Basketball']).suggest()