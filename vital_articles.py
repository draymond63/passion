from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm

import json
import pandas as pd
from general import VITALS, VITALS_JSON

def get_title(tag):
    return tag.text.split('(')[0].strip()


def get_vitals(level=4):
    assert level == 4, 'Only level 4 works at the moment'
    base_url = f'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/{level}/'
    uris = ( # ! FOR LEVEL 4
        'People',
        'History',
        'Geography',
        'Arts',
        'Philosophy_and_religion',
        'Everyday_life',
        'Society_and_social_sciences',
        'Biology_and_health_sciences',
        'Physical_sciences',
        'Technology',
        'Mathematics'
    )
    ignore = ('edit', 'Level 1', 'Level 2', 'Level 3', 'Navigation menu', 'Contents', '')
    levels = {}

    for uri in tqdm(uris):
        # Get data from wikipedia
        response = get(base_url + uri)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Start adding data to the levels dict
        levels[uri] = {}
        last_h2 = None
        last_h3 = None
        # Descendants gets access to all tags, children is only surface level
        for tag in soup.descendants:
            # Get broad categories
            if tag.name == 'h2':
                title = get_title(tag)
                if title not in ignore: # Ignore ToC
                    levels[uri][title] = {} 
                    # Keep track of which category we are analyzing
                    last_h2 = title
                    last_h3 = 'DEFAULT' # Some don't have a subcategories
            # Get subcategories
            if tag.name == 'h3' and last_h2:
                title = get_title(tag)
                if title not in ignore: # Ignore ToC
                    levels[uri][last_h2][title] = {}
                    last_h3 = title
            # Get wiki articles
            if tag.name == 'a' and last_h3:
                title = get_title(tag)
                site = tag['href'].split('/')[-1]
                # * END
                if title == 'v':
                    break
                # Add a default category if required
                if last_h3 == 'DEFAULT':
                    levels[uri][last_h2]['DEFAULT'] = {}
                # Add the title if it isn't one that should be ignored
                if title not in ignore:
                    levels[uri][last_h2][last_h3][title] = site
    
    with open(VITALS_JSON, 'w') as f:
        json.dump(levels, f)
    return levels


def levels_to_df():
    with open(VITALS_JSON) as f:
        levels = json.load(f)
    df = {
        'l3': [],
        'l2': [],
        'l1': [],
        'name': [],
        'site': [],
    }

    for l1 in levels:
        for l2 in levels[l1]:
            for l3 in levels[l1][l2]:
                for name in levels[l1][l2][l3]:
                    df['l1'].append(l1)
                    df['l2'].append(l2)
                    df['l3'].append(l3 if l3 != 'DEFAULT' else l2)
                    df['name'].append(name)
                    df['site'].append(levels[l1][l2][l3][name])
    df = pd.DataFrame(df)
    print(df.head())
    print(df.shape)
    df.to_csv(VITALS, index=False)

if __name__ == "__main__":
    get_vitals()
    levels_to_df()

