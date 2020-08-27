import pandas as pd

# * The number of times an item has to be seen for it to be included
rep_times = 3

### Kaggle import: https://github.com/Kaggle/kaggle-api
# kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data
df = pd.read_csv(r'./dump.csv')

# Filter for useful entries 
df = df.filter(items=['memberUrn', 'posTitle', 'startDate', 'endDate'])
# Simplify the member id
df['memberUrn'] = df['memberUrn'].apply(lambda x: int(x.split(':')[-1]))
# Lowercase every job
df['posTitle'] = df['posTitle'].str.lower()
# Remove entries that don't appear that often
df = df[df.groupby('posTitle')['posTitle'].transform('count') >= rep_times]
df = df.drop_duplicates()

df.to_csv('./dump_cleaned.csv')

print(df.head())
