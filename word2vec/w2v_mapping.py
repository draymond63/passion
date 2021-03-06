import subprocess
import os
import pandas as pd
import numpy as np
from tqdm import tqdm

from Passion.word2vec.test_embedding import evaluate
from Passion.general import get_clean_dump
from Passion.general import SPACE_DIM, W2V_MATRIX
file_data = 'word2vec/temp/data.txt'
file_wv = 'word2vec/temp/wv.txt'
file_cv = 'word2vec/temp/cv.txt'

# * Runs the subroutine
def generate_embedding(**arg_dict):
    output = "word2vec/temp/vecs_{p1}_{p2}.txt".format(**arg_dict)
    command = "word2vec\\word2vecf.exe -output {} -train {file_data} -wvocab {file_wv} -cvocab {file_cv} -threads 150 -alpha {alpha} -size {size} -{param1} {p1} -{param2} {p2}".format(output,**arg_dict)
    if not os.path.exists(output):
        print(f"\t * Starting {output}")
        subprocess.run(command, shell=True)
    return output

# * Grabs output from the subroutine
def load_embedding(filepath,split=False, **kwargs):
    # Skiprows because shape is the first line
    embedding = pd.read_csv(filepath, sep=' ', header=None, skiprows=1, **kwargs)
    embedding.set_index(0)
    embedding = embedding.rename(columns={0: 'site'})
    wikis, vectors = embedding.iloc[:, 0], embedding.iloc[:, 1:151]
    vectors = vectors.divide(np.linalg.norm(vectors, axis=1), axis=0)
    if split:
        return wikis, vectors
    embedding = pd.concat([wikis, vectors], axis=1).set_index('site')
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
    context_vocab.to_csv(file_cv, sep=' ', header=False)


def create_w2v_map():
    # Word2vec parameters, using negative sampling
    embedding_args = {
        "param1": "sample", 
        "param2": "negative", 

        "file_data": file_data ,
        "file_wv": file_wv,
        "file_cv": file_cv,

        "size": SPACE_DIM,
        "alpha": 0.18
    }
    # We are unsure which one of these params will be the best, so we are going to iterate through them
    p1_vals = [format(x, '.4f') for x in np.linspace(0.001, 0.01, 11)]
    p2_vals = np.linspace(15,95,11)
    embedding_fps = [] # File paths generated by the binary
    for p1 in p1_vals:
        for p2 in p2_vals:
            filename = generate_embedding(p1=p1,p2=p2,**embedding_args)
            embedding_fps.append(filename)
    # Load possible matrices into dataframes
    embedding_dfs = list(map(load_embedding, tqdm(embedding_fps)))
    # Evaluate embeddings
    results = [evaluate(df) for df in tqdm(embedding_dfs)]
    idx = results.index(max(results))
    # Best file is word2vec/temp/vecs_0.0055_55.0.txt at 6.25 %
    print('Best file is', embedding_fps[idx], 'at', max(results)*100, '%')
    # Return the winner!
    winner = embedding_dfs[idx]
    winner.to_csv(W2V_MATRIX)



if __name__ == '__main__':
    # file_prep()
    create_w2v_map()
    