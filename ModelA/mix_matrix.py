import pickle

import Data.confusion_matrix_png as cmp
from keras.layers import Dense, BatchNormalization, Activation
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
    BatchNormalization(input_shape = (1000,)),
    Activation('relu'),
    Dense(1000),
    Dense(500),
    Dense(500),
    Dense(500),
    Dense(500),
    Dense(250),
    Dense(125),
    Dense(60),
    Dense(31,activation='softmax')
])
model.load_weights("model.h5")

out = model.predict(test_x,batch_size=200)
y_pred = lb.inverse_transform(out)
y_true = lb.inverse_transform(test_y)
C2 = confusion_matrix(y_true, y_pred, labels=lb.classes_.tolist())

cm = C2
classlist =  lb.classes_
cmp.ConfusionMatrixPng(cm,classlist.tolist())

