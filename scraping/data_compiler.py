from json import load
from pandas import DataFrame
from tqdm import tqdm
import os

# print(len(os.listdir('./crawledProfiles'))) # 410

# * Initial starting profiles
# "https://www.linkedin.com/in/draymond63/",
# "https://www.linkedin.com/in/smbankole/",
# "https://www.linkedin.com/in/isabel-ql-07a2aa90/",
# "https://www.linkedin.com/in/chidinwaogu/",
# "https://www.linkedin.com/in/ngen-sophorn-4075a2155/"

jobs = DataFrame(columns=['user_id', 'posTitle', 'startDate', 'endDate'])

directory = './scraping/crawledProfiles'
pbar = tqdm(total=len(os.listdir(directory)))

for filename in os.listdir(directory):
    user_id = filename[:-5] # Remove file extension

    with open(f'{directory}/{filename}', 'r', encoding='utf-8') as json_file:
        data = load(json_file)

    # Grab only the positions
    posData = data['positions']
    
    # Iterate through each job
    for job in posData:
        # Make sure the data that we want is there
        if 'date1' in job and 'title' in job:
            # Grab the relevant info
            posTitle = job['title']
            dates = job['date1'].split('–')

            # Only grab it if the date has a beginning and end
            if len(dates) == 2:
                startDate = dates[0].strip()
                endDate = dates[1].strip()
                # Append it to the dataframe
                jobs = jobs.append({
                    'user_id': user_id, 
                    'posTitle': posTitle, 
                    'startDate': startDate, 
                    'endDate': endDate
                }, ignore_index=True)

    pbar.update()

jobs.to_csv('../dump2.csv')

print(jobs.head())
