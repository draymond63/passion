### Kaggle import: https://github.com/Kaggle/kaggle-api
# kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data

from data_cleaning import clean_data
from tfidf import tfidf_cluster

from tfidf.tfidf_vectorizer import tfidf_vecs
from path.career_path_compile import compile_prereq_graph

CREATE_DATA = True
CREATE_PATH_GRAPH = True

if __name__ == "__main__":
    # * Clean the data and assign key tags to each job (based off term frequency)
    if CREATE_DATA:
        clean_data()                # rep_times = 3
        tfidf_vecs()                # min_doc_freq = 0.001
        # Defaults to appending tfidf keys
        tfidf_cluster.append_keys() # cluster_threshold = 1

    # * Use this graph in the path_test & path_use files
    if CREATE_PATH_GRAPH:
        compile_prereq_graph()

    # * Creates an N-D map of the careers based on who had what jobs
              


