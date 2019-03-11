import pickle

import Data.confusion_matrix_png as cmp
from keras.layers import Dense, BatchNormalization, Activation,Embedding,CuDNNGRU
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
    BatchNormalization(),
    Activation('relu'),
    CuDNNGRU(64),
    Dense(1024, activation="relu"),
    Dense(31, activation='softmax')
])
model.load_weights("model.h5")

out = model.predict(test_x,batch_size=200)
y_pred = lb.inverse_transform(out)
y_true = lb.inverse_transform(test_y)
count = 0
tokenizer = joblib.load('../steps/tokenizer.model')
for i in range(len(y_true)):
    if y_pred[i] != y_true[i]:
        print(tokenizer.sequences_to_texts([test_x[i].tolist()]))
        count += 1
print (count)
C2 = confusion_matrix(y_true, y_pred, labels=lb.classes_.tolist())

cm = C2
classlist =  lb.classes_
cmp.ConfusionMatrixPng(cm,classlist.tolist())

