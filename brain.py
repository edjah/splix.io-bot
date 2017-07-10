import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import keras.backend as K

MAX_PLAYERS = 10
MAX_TRAIL = 50
VIEW_RADIUS = 10
VEC_SIZE = 1 + MAX_PLAYERS * (MAX_TRAIL * 2 + 5) + (2 * VIEW_RADIUS + 1) ** 2
print('VECTOR SIZE:', VEC_SIZE)

def game_update_to_vector(update):
    players = update['players'][:MAX_PLAYERS]
    vector = np.zeros(1 + MAX_PLAYERS * (MAX_TRAIL * 2 + 5))
    vector[0] = players[0]['skinBlock']
    i = 1

    for player in players:
        vector[i] = int(player['deathWasCertain'])
        vector[i + 1] = player['dir']
        vector[i + 2] = int(player['isMyPlayer'])
        vector[i + 3] = player['pos'][0]
        vector[i + 4] = player['pos'][1]
        i += 5

        if len(player['trails']) > 0:
            trails = player['trails'][0]['trail']
            trails = trails[:MAX_TRAIL]
            for j in range(len(trails)):
                vector[i + 2 * j] = trails[j][0]
                vector[i + 2 * j + 1] = trails[j][1]
        i += MAX_TRAIL * 2

    blocks = update['blocks']
    x, y = map(round, players[0]['pos'])
    grid = np.full((2 * VIEW_RADIUS + 1, 2 * VIEW_RADIUS + 1), -1)

    for block in blocks:
        bx, by = block['x'] - x, block['y'] - y
        cur = block['currentBlock']
        if cur >= 15:
            cur -= 15
        elif 2 <= cur < 15:
            cur -= 2

        if -VIEW_RADIUS <= bx <= VIEW_RADIUS and -VIEW_RADIUS <= by <= VIEW_RADIUS:
            grid[bx][by] = cur

    return np.append(vector, grid.flatten())

class NeuralNetwork:
    def __init__(self, input_size=VEC_SIZE, output_size=5, hidden=None, activation='relu', dropout=0.0):
        hidden = hidden or []
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
        if update and all(x for x in update.values()):
            vec = game_update_to_vector(update)
            prediction = self.model.predict(vec.reshape(1, -1))
            return np.argmax(prediction[0])
        return None

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
