### Kaggle import: https://github.com/Kaggle/kaggle-api
# kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data

from data_cleaning import clean_data
from tfidf import tfidf_cluster

from tfidf.tfidf_vectorizer import tfidf_vecs
from path.career_path_compile import compile_prereq_graph

from w2v.w2v_train_compile import compile_w2v_data
from w2v.w2v_career_map import create_w2v_map, display_map
from w2v import w2v_cluster

CREATE_DATA = True
CREATE_PATH_GRAPH = True
CREATE_W2V_MAP = True
DISPLAY_W2V_MAP = False

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
    if CREATE_W2V_MAP:
        compile_w2v_data()
        create_w2v_map()            # space_dim = 25
        w2v_cluster.append_keys()
    if DISPLAY_W2V_MAP:
        display_map()

