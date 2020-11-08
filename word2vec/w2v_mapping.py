import subprocess
import os
import pandas as pd
import numpy as np
from tqdm import tqdm

from Passion.general import get_clean_dump
from Passion.general import SPACE_DIM
file_data = 'word2vec/data.txt'
file_wv = 'word2vec/wv.txt'
file_cv = 'word2vec/cv.txt'

# * Runs the subroutine
def generate_embedding(**arg_dict):
    output = "word2vec/vecs_{p1}_{p2}.txt".format(**arg_dict)
    command = "word2vec\word2vecf.exe -output {} -train {file_data} -wvocab {file_wv} -cvocab {file_cv} -threads 150 -alpha {alpha} -size {size} -{param1} {p1} -{param2} {p2}".format(output,**arg_dict)
    print(command)
    if not os.path.exists(output):
        print(f"\t * Starting {output}")
        subprocess.run(command, shell=True)
    return output

def load_embedding(filepath,split=True, **kwargs):
    embedding = pd.read_csv(filepath, sep=' ', header=None, skiprows=1, **kwargs)
    embedding.set_index(0)
    embedding = embedding.rename(columns={0: 'subreddit'})
    subreddits, vectors = embedding.iloc[:, 0], embedding.iloc[:, 1:151]
    vectors = vectors.divide(np.linalg.norm(vectors, axis=1), axis=0)
    if split:
        return subreddits, vectors
    embedding = pd.concat([subreddits, vectors], axis=1).set_index("subreddit")
    return embedding

# * All files need to be space separated txt files
def file_prep():
    # Read in and organize data
    training_data = get_clean_dump()
    word_vocab = training_data.groupby('site')['amt'].agg(sum)
    context_vocab = training_data.groupby('ref')['amt'].agg(sum)

    training_data = training_data.drop('type', axis=1)
    # Save all to txt files with values separated by spaces
    training_data.to_csv(file_data, sep=' ', header=False, index=False)
    word_vocab.to_csv(file_wv, sep=' ', header=False)
    context_vocab.to_csv(file_wv, sep=' ', header=False)


def create_w2v_map():# Word2vec parameters, using negative sampling
    # -alpha 0.18 -negative 35 -sample 0.0043 -size 150
    embedding_args = {
        "param1": "sample", 
        "param2": "negative", 
        "file_data": file_data , # data.txt : training_data -> DOWNLOADED DATA (kind of)
                                    # +------------------+--------------------+-----+
                                    # |         subreddit|              author|count|
                                    # +------------------+--------------------+-----+
                                    # |               wsb|            oncutter|    2|
                                    # |       apexlegends|IShouldWashTheDishes|   83|
        "file_wv": file_wv,      # wv.txt   : word_vocabulary -> Wiki totals
                                    # +--------------------+-------+
                                    # |           subreddit|  count|
                                    # +--------------------+-------+
                                    # |              soccer|9419831|
                                    # |               ffxiv|1961764|
        "file_cv": file_wv,      # cv.txt   : context_vocabulary (Same as the word vocabulary since wikis are the context)
                                    
        "size": SPACE_DIM,
        "alpha": 0.18
    }
    # We are unsure which on of these will be the best, so we are going to iterate through them
    # p1_vals = list(map(lambda x : format(x,'.4f'),np.linspace(0.001,0.01,11)))
    # p2_vals = np.linspace(15,95,11)
    p1_vals = [0.001]
    p2_vals = [15.0]
    for p1 in p1_vals:
        for p2 in p2_vals:
            embedding_fps = generate_embedding(p1=p1,p2=p2,**embedding_args)
    
    embedding_dfs = list(map(lambda e : load_embedding(e,split=False), tqdm(embedding_fps)))

    print(embedding_dfs)



if __name__ == '__main__':
    file_prep()
    create_w2v_map()
    