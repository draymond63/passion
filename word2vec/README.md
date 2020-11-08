### All files in the src directory have been cloned from https://github.com/CSSLab/Political-Subreddit-Embedding

This is a modification of the word2vec software by Mikolov et.al, allowing:
   - performing multiple iterations over the data.
   - the use of arbitraty context features.
   - dumping the context vectors at the end of the process.

This software was used in the paper "Dependency-Based Word Embeddings", Omer
Levy and Yoav Goldberg, 2014.

The "main" binary is word2vecf. See below for usage
instructions.

Unlike the original word2vec program which is self-contained,
the word2vecf program assumes some precomputations.

In particular, word2vecf DOES NOT handle vocabulary construction, and does
not read an unprocessed input.

The expected files are:
word_vocabulary:
   file mapping words (strings) to their counts
context_vocabulary:
   file mapping contexts (strings) to their counts
   used for constructing the sampling table for the negative training.
training_data:
   textual file of word-context pairs.
   each pair takes a seperate line.
   the format of a pair is "<word> <context>", i.e. space delimited, where <word> and <context> are strings.
   if we want to prefer some contexts over the others, we should construct the
   training data to contain the bias.

(content below is the README.txt file of the original word2vec software)

Tools for computing distributed representtion of words
------------------------------------------------------

We provide an implementation of the Continuous Bag-of-Words (CBOW) and the Skip-gram model (SG), as well as several demo scripts.

Given a text corpus, the word2vec tool learns a vector for every word in the vocabulary using the Continuous
Bag-of-Words or the Skip-Gram neural network architectures. The user should to specify the following:
 - desired vector dimensionality
 - the size of the context window for either the Skip-Gram or the Continuous Bag-of-Words model
 - training algorithm: hierarchical softmax and / or negative sampling
 - threshold for downsampling the frequent words 
 - number of threads to use
 - the format of the output word vector file (text or binary)

Usually, the other hyper-parameters such as the learning rate do not need to be tuned for different training sets. 

The script demo-word.sh downloads a small (100MB) text corpus from the web, and trains a small word vector model. After the training
is finished, the user can interactively explore the similarity of the words.

More information about the scripts is provided at https://code.google.com/p/word2vec/


# Word2vecf Binary Usage

Producing embeddings with word2vecf:
====

There are three stages:

      1. Create input data, which is in the form of (word,context) pairs.
         the input data is a file in which each line has two space-separated items, 
         first is the word, second is the context.

         for example, in order to create syntactic contexts based on a dependency 
         parsed data in conll format:

            cut -f 2 conll_file | python scripts/vocab.py 50 > counted_vocabulary
            cat conll_file | python scripts/extract_deps.py counted_vocabulary 100 > dep.contexts

         (This part will take a while, and produce a very large file.)

         the first line counts how many times each word appears in the conll_file, 
         keeping all counts >= 50

         the second line extracts dependency contexts from the parsed file,
         skipping either words or contexts with words that appear < 100 times in
         the vocabulary.  (Note: currently, the `extract_deps.py` script is lowercasing the input.)

      1.5 If you want to perform sub-sampling, or prune away some examples, now will be a good time
          to do so.

      2. Create word and context vocabularies:

            ./myword2vec/count_and_filter -train dep.contexts -cvocab cv -wvocab wv -min-count 100

         This will count the words and contexts in dep.contexts, discard either words or contexts
         appearing < 100 times, and write the counted words to `wv` and the counted contexts to `cv`.
      
      3. Train the embeddings:
         
            ./myword2vec/word2vecf -train dep.contexts -wvocab wv -cvocab cv -output dim200vecs -size 200 -negative 15 -threads 10

         This will train 200-dim embeddings based on `dep.contexts`, `wv` and `cv` (lines in `dep.contexts` with word not in `wv` or context
         not in `cv` are ignored).
         
         The -dumpcv flag can be used in order to dump the trained context-vectors as well.

            ./myword2vec/word2vecf -train dep.contexts -wvocab wv -cvocab cv -output dim200vecs -size 200 -negative 15 -threads 10 -dumpcv dim200context-vecs


      3.5 convert the embeddins to numpy-readable format:
         
            ./scripts/vecs2nps.py dim200vecs vecs

          This will create `vecs.npy` and `vecs.vocab`, which can be read by
          the infer.py script.
