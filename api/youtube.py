# https://developers.google.com/explorer-help/guides/code_samples#python
# https://developers.google.com/youtube/v3/docs/playlists/list

from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from json import load

import pandas as pd
import nltk 

class YouTubeApi():
    def __init__(self):
        # Grab secrets that shouldn't be on GitHub ;)
        with open('api/secret_file.json', 'r') as content:
            secrets = load(content)
        # Build the youtube API for public data (no Oauth)
        self.yt = build('youtube', 'v3', developerKey=secrets['devKey'])

        nltk.download('words', raise_on_error=True)
        self.english = set(nltk.corpus.words.words())

    # Quota cost: 100
    def get_playlists(self, search_req: str, is_playist=True) -> dict:
        # Pull request
        request = self.yt.search().list(
            part='snippet', # 'id, title, description'
            maxResults=25,
            relevanceLanguage='en',
            type='playlist' if is_playist else None,
            q=search_req
        )
        response = request.execute()
        # Extract wanted data
        ids = [item['id']['playlistId'] for item in response['items']]
        titles = [item['snippet']['title'] for item in response['items']]

        return {
            'id': ids,
            'title': titles
        }

    # Quota cost: 1
    def playlist_to_videos(self, playlist_id: int) -> dict:
        # Make the request for the videos in the playlist
        request = self.yt.playlistItems().list(
            part='snippet',
            playlistId=playlist_id
        )
        response = request.execute()
        items = response['items']

        # Gather wanted data
        ids = [item['id'] for item in items]
        titles = [item['snippet']['title'] for item in items]
        descs = [item['snippet']['description'] for item in items]

        return {
            'id': ids,
            'title': titles,
            'description': descs
        }

    def strip_to_english(self, words: list) -> list:
        new_words = []

        for sentence in words:
            better = [w for w in nltk.wordpunct_tokenize(sentence) if w.lower() in self.english or not w.isalpha()]
            print(better)
            s = ' '.join(better)

            if s:
                new_words.append(s)
        return new_words

    def vectorize_words(self, words: list) -> pd.DataFrame:
        v = TfidfVectorizer(min_df=0.01, stop_words=['by', 'my'])
        x = v.fit_transform(words)

        tfidfs = pd.DataFrame(x.todense(), columns=v.vocabulary_.keys())
        words = pd.Series(words, name='video_info')
        return tfidfs.join(words)

    def get_path(self, goal: str):
        # # Get most relevant playlists
        # playlists = self.get_playlists(goal + ' tutorial')

        # # Gather all the titles and descriptions from all the playlists retrieved
        # videos = []
        # for i in playlists['id']:
        #     data = self.playlist_to_videos(i)
            
        #     for title, desc in zip(data['title'], data['description']):
        #         video = title + ' ' + desc
        #         videos.append(video)

        videos = [
            'yasin_shahp hello',
            'yasin_shahp',
            'yup this makes sense'
        ]

        videos = self.strip_to_english(videos)
        print('yup' if 'make' in self.english else 'nope')
        print(videos)
        # keys = self.vectorize_words(videos)
        # print(keys.head())


if __name__ == "__main__":
    yt = YouTubeApi()
    yt.get_path('soccer juggling')