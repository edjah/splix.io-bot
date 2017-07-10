import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import keras.backend as K

class NeuralNetwork:
    def __init__(self, input_size, output_size, hidden, activation='relu', dropout=0.0):
        model = Sequential()
        if len(hidden) == 0:
            model.add(Dense(output_size, input_shape=(input_size,), activation='softmax'))
        else :
            model.add(Dense(hidden[0], input_shape=(input_size,), activation=activation))
            for layer_size in hidden[1:-1]:
                model.add(Dense(layer_size, activation=activation))
                if dropout > 0:
                    model.add(Dropout(dropout))
            model.add(Dense(output_size, activation='softmax'))

        model._make_predict_function()
        self.model = model

    def update(self, update):
        prediction = self.model.predict(update.reshape(1, -1))
        return np.argmax(prediction[0])

class Stalker:
    def __init__(self, target_name):
        self.target_name = target_name

    def update(self, update):
        players = update['players']
        target = next((p for p in players if p['name'] == self.target_name), None)
        if target:
            return target['dir']
        else:
            return None


if __name__ == '__main__':
    import time
    n = 2000
    b = NeuralNetwork(n, 5, [512, 512])
    update = np.arange(n)
    start = time.time()
    print(b.update(update))
    end = time.time()
    print('{} sec'.format(end - start))
    K.clear_session()
