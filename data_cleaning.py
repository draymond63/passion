import pandas as pd
from nltk import word_tokenize, download
from nltk.stem import WordNetLemmatizer
download(['punkt', 'wordnet'])

replacements = {
    'cio': 'chief information officer', 
    'ceo': 'chief information officer', 
    'cfo': 'chief executive officer', 
    'coo': 'chief financial officer', 
    'cmo': 'chief marketing officer', 
    'cto': 'chief technology officer', 
    '-': '', 
    'bi': 'business intelligence', 
    'dba': 'database administrator', 
    'qa': 'quality assurance', 
    'pmo': 'project management office', 
    'pr': 'public relations', 
    'hr': 'human resources', 
    'sr': 'senior', 
    'vp': 'vice president', 
    'adviser': 'advisor', 
    'sap': 'system applications', 
    'leader': 'manager', 
    'lead': 'manager'
}

def lemmatize(item: str) -> str:
    wordnet_lemmatizer = WordNetLemmatizer()
    # Break the string into a list of words
    words = word_tokenize(item)
    # Reduce each word to a lemma
    for i, word in enumerate(words):                    
        new_word = wordnet_lemmatizer.lemmatize(word)
        words[i] = new_word
    # Replace the entry with the final item
    new_item = ' '.join(words)
    return new_item

def clean_data(og_file='dump.csv', new_file='dump_cleaned.csv', rep_times=3):
    ### Kaggle import: https://github.com/Kaggle/kaggle-api
    # kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data
    df = pd.read_csv(r'dump.csv')

    # Filter for useful entries 
    df = df.filter(items=['memberUrn', 'posTitle', 'startDate', 'endDate'])
    # Simplify the member id
    df['memberUrn'] = df['memberUrn'].apply(lambda x: int(x.split(':')[-1]))
    # Lowercase every job
    df['posTitle'] = df['posTitle'].str.lower()

    # * Character removal 
    # Remove the end of entries with the following symbols
    df['posTitle'] = df['posTitle'].apply(lambda x: x.split('(')[0])
    df['posTitle'] = df['posTitle'].apply(lambda x: x.split(',')[0])
    df['posTitle'] = df['posTitle'].apply(lambda x: x.split('|')[0])
    df['posTitle'] = df['posTitle'].apply(lambda x: x.split(':')[0])
    df['posTitle'] = df['posTitle'].apply(lambda x: x.split(' - ')[0])
    df['posTitle'] = df['posTitle'].apply(lambda x: x.strip())

    # * Substring Replacement
    # Add regex operators before and after each key to make sure we aren't matching in another word
    # https://stackoverflow.com/questions/6713310/regex-specify-space-or-start-of-string-and-space-or-end-of-string
    reg_repl = {}
    for key in replacements:
        reg_repl[r'(^|\s)' + key+ r'[\b\s]'] = replacements[key]
    df['posTitle'].replace(regex=reg_repl, inplace=True)
    # * Lemmatization
    df['posTitle'] = df['posTitle'].apply(lemmatize)

    # ? Remove columns with 'and' or '&' in them?

    # * Final touches
    # Remove entries that don't appear that often
    df = df[df.groupby('posTitle')['posTitle'].transform('count') >= rep_times]
    # Drop all duplicates and the NAs except for the end dates
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
    print('Size:', df.memory_usage().sum() // 2**10, 'KiB')

if __name__ == "__main__":
    clean_data()