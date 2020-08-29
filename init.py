### Kaggle import: https://github.com/Kaggle/kaggle-api
# kaggle datasets download -f dump.csv --unzip killbot/linkedin-profiles-and-jobs-data

from data_cleaning import clean_data
from tfidf.tfidf_vectorizer import tfidf_vecs
from tfidf.tfidf_clustering import append_dump
from path.career_path_compile import compile_prereq_graph


CREATE_DATA = True
CREATE_PATH_GRAPH = False
CREATE_W2V_MAP = False

if __name__ == "__main__":
    # * Clean the data and assign key tags to each job (based off term frequency)
    if CREATE_DATA:
        clean_data()
        tfidf_vecs()
        append_dump()

    # * Use this graph in the path_test & path_use files
    if CREATE_PATH_GRAPH:
        compile_prereq_graph()

    # ! Convert jupyter notebooks to py files so they can be imported
    if CREATE_W2V_MAP:
        pass

