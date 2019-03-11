import re

import jieba
from flask import Flask, request,jsonify,render_template
from keras.layers import Dense, BatchNormalization, Activation, Embedding, GRU,CuDNNGRU,MaxPool1D,Conv1D,Flatten,Dropout,Bidirectional
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from sklearn.externals import joblib

restr = r'[0-9\s+\.\!\/_,$%^*();?:\-<>《》【】+\"\']+|[+——！，；。？：、~@#￥%……&*（）]+'

class Region(object):
    def __init__(self):
        self.tokenizer = joblib.load('steps/tokenizer.model')
        self.lb = joblib.load('steps/lb.model')
        self.model = self.cnn_rnn_attention()

    def cnn_rnn_attention(self):
        model = Sequential([
            Embedding(200000 + 1, 128, input_shape=(1000,)),
            BatchNormalization(),
            Activation('relu'),
            CuDNNGRU(64),
            Dense(1024, activation="relu"),
            Dense(31, activation='softmax')
        ])
        model.load_weights('ModelD\\model.h5')
        return model

    def prdected(self, text):
        resu = text.replace('|', '').replace('&nbsp;', '').replace('ldquo', '').replace('rdquo',
                                                                                                          '').replace(
            'lsquo', '').replace('rsquo', '').replace('“', '').replace('”', '').replace('〔', '').replace('〕', '')
        resu = re.split(r'\s+', resu)
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', ''.join(resu))
        line = re.sub(restr, '', dd)
        seg_list = jieba.lcut(line)
        sequences = self.tokenizer.texts_to_sequences([seg_list])
        data = pad_sequences(sequences, maxlen=1000)
        pred = self.model.predict(data, batch_size=len(data))
        return self.lb.inverse_transform(pred)
model_obj = Region()
app = Flask(__name__)

@app.route("/",methods =["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        text = request.form.get("content")
        if (text != "" and text != None):
            result = {"result":model_obj.prdected(text)[0],"status":"1"}
        else:
            result = {"result":"DateType_error","status":"0"}
        return jsonify(result)
app.run(host = "0.0.0.0", port = 80, debug = True, use_reloader = False)
