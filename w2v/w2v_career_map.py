import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras

def create_w2v_map(og_file='w2v/w2v_train.json', new_file='w2v/pos_w2v_matrix.json', space_dim=25):
    print('\nCREATING W2V MAP')
    train = pd.read_json(og_file)

    print(train.head())

    num_users = len(train['members'][0])
    num_jobs = train.shape[0]
    # Simple 2 layer model to create the word2vec matrix
    # Predicting word (job) based off context (members who had that job) currently
    # people --> job
    model = keras.models.Sequential([
        keras.layers.Dense(space_dim, input_dim=num_users),
        keras.layers.Dense(num_jobs, activation='softmax')
    ])
    # Hyper parameters
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    model.summary()

    # * Train the model
    history = model.fit(
        np.array(train['members'].tolist()), # dtype=np.float32
        np.array(train['posEncoded'].tolist()),
        callbacks=[
            tf.keras.callbacks.EarlyStopping(monitor='accuracy', min_delta=0.0001, patience=10)
        ],
        epochs=200,
        shuffle=True,
        verbose=0
    )
    print('Model Accuracy:', history.history['accuracy'][-1] * 100, '%')

    # * Store the w2v matrix with the titles
    w2v_matrix = pd.DataFrame(model.get_weights()[2]).transpose()
    w2v_matrix = pd.concat([train['posTitle'], w2v_matrix], axis=1)
    w2v_matrix.to_json(new_file)


def display_map(og_file='w2v/pos_w2v_matrix.json', title_options='', dump_file='dump_cleaned.csv'):
    # We need to shrink the dimensionality and display it
    from sklearn.manifold import TSNE
    import plotly.express as px
    data = pd.read_json(og_file)
    # get_weights returns weights & biases -> we want the 2nd matrix of weights (w2v_inner_dim by # of jobs)
    w2v_matrix = data.drop(['posTitle'], axis=1)
    titles = data['posTitle']

    # Collapse matrix into Nx2
    tsne = TSNE(n_components=2, random_state=0)
    w2v_visual = tsne.fit_transform(w2v_matrix)

    dump = pd.read_csv(dump_file)
    w2v_visual = pd.DataFrame(w2v_visual, columns=['x', 'y'])
    # Reattach the titles
    df = w2v_visual.join(data['posTitle'])
    # Attach the w2v groups
    df = pd.merge(dump, df, on='posTitle')
    df = df.filter(['posTitle', 'x', 'y', 'w2vKeyNum'])
    df = df.drop_duplicates()

    print(df.head(3))

    # Display data
    fig = px.scatter(df,
        x='x', y='y',
        hover_name='posTitle', # ? Apparently labels are wrong ?
        color='w2vKeyNum'
    )
    fig.update_layout(title='Word2Vec 2D Career Map ' + title_options)
    fig.show()

if __name__ == "__main__":
    # create_w2v_map(space_dim=25)
    display_map()
