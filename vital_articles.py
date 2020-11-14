from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm

import json
import pandas as pd
from general import VITALS, VITALS_URI, VITALS_JSON

def get_title(tag):
    return tag.text.split('(')[0].strip()

def parse_uri(storage, base_url, uri, name=None):
    if not name:
        name = uri
    ignore = ('edit', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Navigation menu', 'Contents', 'Back to contents', '')
    # Get data from wikipedia
    response = get(base_url + uri)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Start adding data to the levels dict
    storage[name] = {}
    group = storage[name] # Simplifying pointer
    last_h = {1: name, 2: None, 3: None} # h1-3
    # print('G:', name)
    # Descendants gets access to all tags, children is only surface level
    for tag in soup.descendants:
        # Get Large categories (mainly for level 5)
        if tag.name == 'h1':
            title = get_title(tag)
            if not title:
                print('h1', tag, title)
            if 'Wikipedia' not in title:
                group[title] = {}
                last_h = {1: title, 2: title, 3: title} # Reset header values
                # print('\tH1:', title)
        # Get broad categories
        elif tag.name == 'h2':
            title = get_title(tag)
            if not title:
                print('h2', tag, title) 
            if title not in ignore: # Ignore ToC
                if last_h[1] not in group:
                    group[last_h[1]] = {}
                group[last_h[1]][title] = {} 
                # Keep track of which category we are analyzing
                last_h[2] = title
                last_h[3] = title # Some don't have a subcategories
                # print('\t\tH2:', title)
        # Get subcategories
        elif tag.name == 'h3' and last_h[2]:
            title = get_title(tag)
            if not title:
                print('h3', tag, title)
            if title not in ignore: # Ignore ToC
                # Add a default category if required
                if last_h[2] not in group[last_h[1]]:
                     group[last_h[1]][last_h[2]] = {}
                group[last_h[1]][last_h[2]][title] = {}
                last_h[3] = title
                # print('\t\tH3:', title)
        # Get wiki articles
        elif tag.name == 'a' and last_h[3]:
            title = get_title(tag)
            site = tag['href'].split('/')[-1]
            # * END
            if title == 'v':
                break
            # Add the title if it isn't one that should be ignored
            if title not in ignore:
                # Add a default category if required
                if last_h[2] not in group[last_h[1]]:
                     group[last_h[1]][last_h[2]] = {}
                if last_h[3] not in group[last_h[1]][last_h[2]]:
                    group[last_h[1]][last_h[2]][last_h[3]] = {}
                # Add the wiki!
                group[last_h[1]][last_h[2]][last_h[3]][title] = site


def get_vitals(level=4):
    base_url = f'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/{level}/'
    with open(VITALS_URI) as f:
        uris = json.load(f)[str(level)]
    
    levels = {}
    if level == 4:
        for uri in tqdm(uris):
            parse_uri(levels, base_url, uri)

    elif level == 5: # ! GET RID OF NULLS IN vitals.json
        # uris = {"Mathematics": "Mathematics"}
        for area in tqdm(uris):
            levels[area] = {}
            if isinstance(uris[area], list):
                for uri in uris[area]:
                    # Dumb work around for it
                    if uris[area] != ['Everyday_life']:
                        parse_uri(levels[area], base_url, f'{area}/{uri}', uri)
                    else:
                        parse_uri(levels[area], base_url, uri)
            else:
                parse_uri(levels[area], base_url, uris[area])

    
    for l0 in levels:
        for l1 in levels[l0]:
            for l2 in levels[l0][l1]:
                if not l2:
                    print(l0, l1, l2)
                            
    with open(VITALS_JSON, 'w') as f:
        json.dump(levels, f)
    return levels

def levels_to_df_5():
    with open(VITALS_JSON) as f:
        levels = json.load(f)
    df = {
        'l0': [],
        'l1': [],
        'l2': [],
        'l3': [],
        'l4': [],
        'name': [],
        'site': [],
    }
    for l0 in levels:
        for l1 in levels[l0]:
            for l2 in levels[l0][l1]:
                for l3 in levels[l0][l1][l2]:
                    for l4 in levels[l0][l1][l2][l3]:
                        for name in levels[l0][l1][l2][l3][l4]:
                            df['l0'].append(l0)
                            df['l1'].append(l1)
                            df['l2'].append(l2)
                            df['l3'].append(l3)
                            df['l4'].append(l4)
                            df['name'].append(name)
                            df['site'].append(levels[l0][l1][l2][l3][l4][name])
    df = pd.DataFrame(df)
    print(df.sample(5))
    print(df.shape)
    df.to_csv(VITALS, index=False)

def levels_to_df_4():
    with open(VITALS_JSON) as f:
        levels = json.load(f)
    df = {
        'l1': [],
        'l2': [],
        'l3': [],
        'l4': [],
        'name': [],
        'site': [],
    }
    for l1 in levels:
        for l2 in levels[l1]:
            for l3 in levels[l1][l2]:
                for l4 in levels[l1][l2][l3]:
                    for name in levels[l1][l2][l3][l4]:
                        df['l1'].append(l1)
                        df['l2'].append(l2)
                        df['l3'].append(l3)
                        df['l4'].append(l4)
                        df['name'].append(name)
                        df['site'].append(levels[l1][l2][l3][l4][name])
    df = pd.DataFrame(df)
    print(df.sample(5))
    print(df.shape)
    df.to_csv(VITALS, index=False)

def levels_to_df(level=4):
    levels_to_df_4() if level == 4 else levels_to_df_5()

if __name__ == "__main__":
    level = 5
    # get_vitals(level)
    levels_to_df(level)

