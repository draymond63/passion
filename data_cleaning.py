import pandas as pd

def clean_data(og_file='dump.csv', new_file='dump_cleaned.csv'):
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


    # * Remove acronyms
    # ! DOESNT WORK ON SUBSTRINGS
    df['posTitle'] = df['posTitle'].replace(
        ['cio', 'ceo', 'cfo', 'coo', 'cmo', 'cto', 'co-founder', '-', 'bi', 'dba', 'qa', 'pmo', 'pr', 'hr', 'sr', 'vp'],
        ['chief information officer',
        'chief executive officer',
        'chief financial officer',
        'chief operating officer',
        'chief marketing officer',
        'chief technology officer',
        'cofounder',
        '',
        'business intelligence',
        'database administrator',
        'quality assurance',
        'project management office',
        'public relations',
        'human resources',
        'senior',
        'vice president'
        ]
    )

    # * Character removal 
    # Remove the end of entries with the following symbols
    df['posTitle'] = df['posTitle'].apply(lambda x: x.split('(')[0].strip())
    df['posTitle'] = df['posTitle'].apply(lambda x: x.split(',')[0].strip())
    df['posTitle'] = df['posTitle'].apply(lambda x: x.split('|')[0].strip())

    # ? Remove columns with 'and' or '&' in them?

    # * Final touches
    # Remove entries that don't appear that often
    df = df[df.groupby('posTitle')['posTitle'].transform('count') >= rep_times]
    # Drop all duplicates the NAs except for the end dates
    df = df.dropna(subset=['memberUrn', 'posTitle', 'startDate'])
    df = df.drop_duplicates()
    # Sort values just for nicety
    df = df.sort_values(['memberUrn', 'startDate'], ascending=False)
    df = df.reset_index().drop('index', axis=1)
    # Save data
    df.to_csv('dump_cleaned.csv', index=False)
    print('\nCLEANED DATA')
    print(df.head())
    print(df.shape)

if __name__ == "__main__":
    clean_data()