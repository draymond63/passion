### Kaggle import: https://github.com/Kaggle/kaggle-api
# kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data

from data_cleaning import clean_data

from tfidf import tfidf_cluster
from tfidf.tfidf_vectorizer import tfidf_vecs
from tfidf.manual_clean import clean_tfidf_keys

from path.career_path_compile import compile_prereq_graph
from map.career_map_compile import create_career_map, display_map

CREATE_DATA = False
CREATE_PATH_GRAPH = False
CREATE_CMAP = True
DISPLAY_CMAP = True

if __name__ == "__main__":
    # * Clean the data and assign key tags to each job (based off term frequency)
    if CREATE_DATA:
        clean_data()                # rep_times = 3
        tfidf_vecs()                # min_doc_freq = 0.001
        # Defaults to appending tfidf keys
        tfidf_cluster.append_keys() # cluster_threshold = 1
        clean_tfidf_keys()

    # * Use this graph in the path_test & path_use files
    if CREATE_PATH_GRAPH:
        compile_prereq_graph()

    # * Creates an N-D map of the careers based on who had what jobs
    if CREATE_CMAP:
        cmap = create_career_map()  # cluster_threshold = 25, space_dim = 50
    if DISPLAY_CMAP:
        display_map(cmap)


