# Libraries used to train models & manipulate data
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_vects(file_name=None):
    ### Kaggle import: https://github.com/Kaggle/kaggle-api
    # kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data
    pos = pd.read_csv(r'../dump_cleaned.csv')
    # Convert to a series
    pos = pd.Series(pos['posTitle'])

    # * Vectorize position titles using tf-idf (Term frequency -> inverse document frequency)
    # 0.1 -> 2    | 0.01 -> 58    | 0.001 -> 407    | 0 -> 6738
    v = TfidfVectorizer(min_df=0.001) # 0.01 without cell above, 0.001 with
    x = v.fit_transform(pos)
    vecs = pd.DataFrame(x.toarray())

    if file_name:
        vecs.to_csv(file_name) # Save it for other files
    else:
        return vecs

if __name__ == "__main__":
    tfidf_vects('tfidf_positions.csv')