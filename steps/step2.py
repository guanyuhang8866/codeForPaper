from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
import pickle

num_words = 200000
train_list = [i.strip() for i in open('../steps/content.txt', 'r', encoding='utf8')]
try:
    tokenizer = joblib.load('tokenizer.model')
except:
    tokenizer = Tokenizer(num_words=num_words)
    tokenizer.fit_on_texts(train_list)
    joblib.dump(tokenizer,'tokenizer.model')
print(1)
train_list = tokenizer.texts_to_sequences(train_list)
x_train = pad_sequences(train_list, 1000)

label_list = [i.strip() for i in open('../steps/lable.txt', 'r', encoding='utf8')]
try:
    lb = joblib.load('lb.model')
except:
    lb = LabelBinarizer()
    lb.fit(label_list)
    joblib.dump(lb, 'lb.model')
y_train = lb.transform(label_list)

train_x, test_x, train_y, test_y = train_test_split(x_train, y_train, test_size=0.1, random_state=10)
with open("train_data.pkl","wb") as f:
    pickle.dump(train_x, f)
    pickle.dump(train_y, f)
    pickle.dump(test_x, f)
    pickle.dump(test_y, f)