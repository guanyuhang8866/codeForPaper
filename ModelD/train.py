import pickle

from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
from keras.layers import Embedding, Dense, CuDNNGRU, BatchNormalization, Activation
from keras.models import Sequential
from keras.optimizers import Adam

with open("../steps/train_data.pkl","rb") as f:
    train_x = pickle.load(f)
    train_y = pickle.load(f)
    test_x = pickle.load(f)
    test_y = pickle.load(f)

model = Sequential([
    Embedding(200000 + 1, 128, input_shape=(1000,)),
    BatchNormalization(),
    Activation('relu'),
    CuDNNGRU(64),
    Dense(1024, activation="relu"),
    Dense(31, activation='softmax')
])
model.summary()
model.compile(loss = "categorical_crossentropy",optimizer=Adam(lr = 0.001),metrics=['acc'])
save_best = ModelCheckpoint('model.h5', verbose=1, save_best_only=True, save_weights_only=True)
reduce_lr = ReduceLROnPlateau(patience=1, verbose=1, cooldown=1, factor=0.4)
early_stop = EarlyStopping(patience=3, verbose=1)
model.fit(train_x,train_y,epochs=200,batch_size=500,validation_data=(test_x,test_y),callbacks=[early_stop,reduce_lr,save_best])



