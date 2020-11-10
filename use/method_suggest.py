import pandas as pd
import numpy as np
from wiki_suggest import TopicSuggestion

# Method 
class MethodSuggestion(TopicSuggestion):
    def __init__(self, methods=[], words=[]):
        # Just used so the interface will call all init functions
        super(MethodSuggestion, self).__init__(words)
        # Get call list
        funcs = {
            'wiki': self.get_wiki,
            'video': self.get_video,
            'course': self.get_course,
            'book': self.get_book,
            'podcast': self.get_podcast,
            'project': self.get_project,
            'lesson': self.get_lesson
        }
        if len(methods):
            self.methods = {m: funcs[m] for m in methods}
        else:
            self.methods = funcs

    # From category data in wiki_suggest.py
    def get_wiki(self, name):
        return 'https://en.wikipedia.org/wiki/' + self.get_site(name)

    # YT API
    def get_video(self):
        pass
    # Coursera
    def get_course(self):
        pass
    # Library?
    def get_book(self):
        pass
    # Spotify?
    def get_podcast(self):
        pass
    # Udemy? NLP?
    def get_project(self):
        pass
    # Khan/Qiskit?
    def get_lesson(self):
        pass


if __name__ == "__main__":
    user = MethodSuggestion(['wiki'])