from method_suggest import MethodSuggestion

# MethodSuggestion imports from TopicSuggestion
class Suggestion(MethodSuggestion):
    def demo(self, count=3):
        for _ in range(count):
            recommendations = self.recommend_topic()
            print(recommendations)
            selection = recommendations[int(input())]
            # Get summaries if requested
            last_selection = None
            while (selection != last_selection):
                last_selection = selection
                # Show first paragraph
                print(self.get_wiki(selection)['summary'].split('\n')[0])
                print()
                print('Pick a new one?', recommendations)
                selection = recommendations[int(input())]
            # Update user map
            self.select_topic(selection)
            # Send response
            # responses = {key: self.methods[key](selection) for key in self.methods}
            # print(responses)

if __name__ == "__main__":
    Suggestion(
        methods=['wiki'], 
        exclude=['People'],
        words=[
            'Spin', 'Physics', 'Metaphysics', 'Astronomy', 'Neutrino', 
            'Quantum computing', 'ARM architecture', 'IBM'
        ]
    ).demo()