import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras import backend as K
from sklearn.model_selection import train_test_split


# loading the data from a log file
X, y = [], []
with open('game.log', 'r') as f:
    for line in f:
        v = line.rstrip().split(',')
        X.append([float(f) for f in v[:-1]])
        y.append(int(v[-1]))
X = np.array(X)
y = np.eye(5)[y]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# setting up the model architecture. 2 hidden layers of size 128 with relu activation
model = Sequential()
model.add(Dense(128, input_shape=X_train.shape[1:], activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(5, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())


# fitting the model to the training data
model.fit(X_train, y_train, epochs=100, batch_size=10, verbose=2, validation_data=(X_test, y_test))


# evaluating the model on train and test data and displaying out the frequency of actions
train_acc = model.evaluate(X_train, y_train, verbose=0)[1]
test_acc = model.evaluate(X_test, y_test, verbose=0)[1]
train_counts = np.argmax(model.predict(X_train), axis=1)
test_counts = np.argmax(model.predict(X_test), axis=1)
print('Train accuracy: {:.3%} | Test accuracy: {:.3%}'.format(train_acc, test_acc))
print('Train counts:', np.bincount(train_counts))
print('Test counts:', np.bincount(test_counts))


# saving the model
with open('outputs/model.json', 'w') as f:
    f.write(model.to_json())


# serialize weights to HDF5
model.save_weights('outputs/model.h5')

# clear tensorflow session
K.clear_session()

