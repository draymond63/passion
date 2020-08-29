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


def display_map(og_file='w2v/pos_w2v_matrix.json', title_options=''):
    # We need to shrink the dimensionality and display it
    from sklearn.manifold import TSNE
    import plotly.graph_objects as go
    data = pd.read_json(og_file)
    # get_weights returns weights & biases -> we want the 2nd matrix of weights (w2v_inner_dim by # of jobs)
    w2v_matrix = data.drop(['posTitle'], axis=1)
    titles = data['posTitle']

    # Collapse matrix into Nx2
    tsne = TSNE(n_components=2, random_state=0, verbose=1)
    w2v_visual = tsne.fit_transform(w2v_matrix)
    # Display data
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=w2v_visual[:,0], y=w2v_visual[:,1],
        text=titles, # ? Apparently labels are wrong ?
        mode='markers',
        marker_color='rgba(255, 182, 193, .8)'
    ))
    fig.update_layout(title='Word2Vec 2D Career Map ' + title_options)
    fig.show()

if __name__ == "__main__":
    create_w2v_map(space_dim=25)
    display_map()
