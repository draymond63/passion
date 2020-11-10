from method_suggest import MethodSuggestion

# MethodSuggestion imports from TopicSuggestion
class Suggestion(MethodSuggestion):
    # def __init__(self):
    #     super(Suggestion, self).__init__()
    def demo(self):
        recommendations = self.recommend_topic()
        print(recommendations)
        selection = recommendations[int(input())]
        self.select_topic(selection) # Update topic map
        
        responses = {key: self.methods[key](selection) for key in self.methods}
        print(responses)
        return responses


if __name__ == "__main__":
    Suggestion(methods=['video'], words=['Spin']).demo()