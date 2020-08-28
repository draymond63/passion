# Libraries used to train models & manipulate data
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_vecs(file_name=None):
    ### Kaggle import: https://github.com/Kaggle/kaggle-api
    # kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data
    pos = pd.read_csv(r'./dump_cleaned.csv')
    # Convert to a series
    pos = pd.Series(pos['posTitle'])
    pos = pos.drop_duplicates() # There are multiple from each job so remove them
    pos = pos.dropna() # There shouldn't be NAs but there are...
    pos = pos.reset_index()['posTitle'] # Reset the index so things are order 1, 2, 3,...
    print(pos.shape)

    # * Vectorize position titles using tf-idf (Term frequency -> inverse document frequency)
    # 0.1 -> 2    | 0.01 -> 58    | 0.001 -> 407    | 0 -> 6738
    v = TfidfVectorizer(min_df=0.001) # 0.01 without cell above, 0.001 with
    x = v.fit_transform(pos)
    vecs = pd.DataFrame(x.toarray())

    # Save the vocabulary of the Tfidf vectorizer in a list for the df
    vocab = [0] * len(v.vocabulary_)
    for key in v.vocabulary_:
        index = v.vocabulary_[key]
        vocab[index] = key
    
    # Reattach the names to the data
    df = pd.concat([pos, vecs], axis=1)
    # Rename the columns so each tfidf coordinate corresponds to a word
    df.columns = ['posTitle', *vocab]
    print(df.head(3))
    print(df.shape)

    if file_name:
        df.to_csv(f'./tfidf/{file_name}', index=False) # Save it for other files
    return df

if __name__ == "__main__":
    tfidf_vecs('tfidf_positions.csv')