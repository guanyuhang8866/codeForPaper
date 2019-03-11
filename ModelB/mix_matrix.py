import pickle

import Data.confusion_matrix_png as cmp
from keras.layers import Embedding, Dense, MaxPool1D, Conv1D, BatchNormalization, Activation, Flatten
from keras.models import Sequential
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix

with open("../steps/train_data.pkl","rb") as f:
    train_x = pickle.load(f)
    train_y = pickle.load(f)
    test_x = pickle.load(f)
    test_y = pickle.load(f)
lb = joblib.load('../steps/lb.model')
model = Sequential([
    Embedding(200000 + 1, 128, input_shape=(1000,)),
    Conv1D(128, 3, padding='valid'),
    MaxPool1D(pool_size = 4),
    Conv1D(64, 5, padding='valid'),
    MaxPool1D(pool_size = 4),
    Conv1D(31, 5, padding = "valid"),
    MaxPool1D(pool_size = 4),
    BatchNormalization(),
    Activation('relu'),
    # Attention(128),
    Flatten(),
    Dense(1024, activation="relu"),
    Dense(31, activation='softmax')
])
model.load_weights("model.h5")

out = model.predict(test_x,batch_size=200)
y_pred = lb.inverse_transform(out)
y_true = lb.inverse_transform(test_y)
C2 = confusion_matrix(y_true, y_pred, labels=lb.classes_.tolist())

cm = C2
classlist =  lb.classes_
cmp.ConfusionMatrixPng(cm,classlist.tolist())

