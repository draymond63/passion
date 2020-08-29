### Kaggle import: https://github.com/Kaggle/kaggle-api
# kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data

from data_cleaning import clean_data
from tfidf.tfidf_vectorizer import tfidf_vecs
from tfidf.tfidf_clustering import append_dump

from path.career_path_compile import compile_prereq_graph

from w2v.w2v_train_compile import compile_w2v_data
from w2v.w2v_career_map import create_w2v_map

CREATE_DATA = True
CREATE_PATH_GRAPH = True
CREATE_W2V_MAP = True

if __name__ == "__main__":
    # * Clean the data and assign key tags to each job (based off term frequency)
    if CREATE_DATA:
        clean_data()
        tfidf_vecs()
        append_dump()

    # * Use this graph in the path_test & path_use files
    if CREATE_PATH_GRAPH:
        compile_prereq_graph()

    # * Creates an N-D map of the careers based on who had the same job
    if CREATE_W2V_MAP:
        compile_w2v_data()
        create_w2v_map()

