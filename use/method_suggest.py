import pandas as pd
import numpy as np
import json
# Youtube
from googleapiclient.discovery import build
# Key words
import wikipediaapi
# from sklearn.feature_extraction.text import TfidfVectorizer
# from nltk.stem.porter import PorterStemmer
# Personal
from wiki_suggest import TopicSuggestion
from Passion.general import SECRETS

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
        # API Tokens
        with open(SECRETS) as f:
            secrets = json.load(f)
        # Build the youtube API for public data (no Oauth)
        self.yt = build('youtube', 'v3', developerKey=secrets['devKey'])
        # Wikipedia API (For summaries)
        self.wp = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )

    def get_keywords(self, selection):
        site = self.get_site(selection)
        keys = list(self.categories.loc[site].unique())
        # page = self.wp.page(site).text #TODO: Tf-idf with the page text
        return keys

    # From category data in wiki_suggest.py
    def get_wiki(self, selection):
        site = self.get_site(selection)
        summary = self.wp.page(site).summary
        return {
            'summary': summary,
            'link': 'https://en.wikipedia.org/wiki/' + site
        }

    # YT API
    def get_video(self, selection):
        keys = ' '.join(self.get_keywords(selection))
        request = self.yt.search().list(
            part='snippet', # 'id, title, description'
            maxResults=3,
            relevanceLanguage='en',
            type='video',
            videoEmbeddable='true',
            q=keys + ' lesson'
        )
        response = request.execute()
        # Extract wanted data (should also extract IDs)
        base = 'https://www.youtube.com/watch?v='
        links = [base + item['id']['videoId'] for item in response['items']]
        titles = [item['snippet']['title'] for item in response['items']]
        return {
            'link': links,
            'title': titles
        }
    
    # Coursera
    def get_course(self, selection):
        pass
    # Library?
    def get_book(self, selection):
        pass
    # Spotify?
    def get_podcast(self, selection):
        pass
    # Udemy? NLP?
    def get_project(self, selection):
        pass
    # Khan/Qiskit?
    def get_lesson(self, selection):
        pass


if __name__ == "__main__":
    user = MethodSuggestion()
    r = user.get_video('Spin')
    print(r)