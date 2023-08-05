import tensorflow as tf
tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(0)

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import Callback, ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import numpy as np
import pandas as pd

def split_sequence(sequence, n_steps):
    """
    Split a univariate sequence into samples.
    """

    X, y = list(), list()
    for i in range(len(sequence)):
        end_ix = i + n_steps
        if end_ix > len(sequence)-1:
            break
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.asarray(X), np.asarray(y)


def build_model_and_predict(ts_df, column, country_name):

    n_steps = 4  # Number of steps as input; Predict for 1 day
    n_features = 1
    n_test = 1
    X, Y = split_sequence(ts_df[column].values.astype('float32'), n_steps)
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    # prepare train and test dataset -> Last n_test days are for vlaidation
    X_train, X_test, Y_train, Y_test = X[:-
                                         n_test], X[-n_test:], Y[:-n_test], Y[-n_test:]
    minotor = "val_loss"
    c = [
        ModelCheckpoint(country_name+'.hdf5', save_best_only=True,
                        monitor=minotor, mode='min', verbose=0),
        EarlyStopping(monitor=minotor, min_delta=0, patience=600, verbose=0),
        ReduceLROnPlateau(monitor=minotor, factor=0.2,
                          patience=5, min_lr=0.00001)
    ]
    model = Sequential()
    model.add(LSTM(100, activation='relu',
                   kernel_initializer='he_normal', input_shape=(n_steps, 1)))
    model.add(Dense(50, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(50, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(1))

    # compile the model
    model.compile(optimizer='adam', loss='mse',
                  metrics=['mae', 'mse', 'accuracy'])
    
    # # fit the model
    # history = model.fit(X_train, Y_train, epochs=4000, batch_size=32, verbose=0,
    #                     callbacks=c, validation_data=(X_test, Y_test), shuffle=False)
    # evaluate the model

    [mse, mae, loss, accuracy] = model.evaluate(
        X_test, Y_test, batch_size=32, verbose=0)
    print('MSE: %.3f, RMSE: %.3f, MAE: %.3f, ACCURACY: %.3f ' %
          (mse, np.sqrt(mse), mae, accuracy))
    model_performance = pd.DataFrame({'Country': [country_name],
                                        'mae': np.array(mae),
                                        'mse': np.array(mse),
                                        'rmse': np.array(np.sqrt(mse)),
                                        'accuracy': np.array(accuracy)})
    row = np.asarray(ts_df[-n_steps:][column].values.astype('float32')
                     ).reshape((1, n_steps, n_features))
    yhat = model.predict(row)
    return yhat, model_performance


