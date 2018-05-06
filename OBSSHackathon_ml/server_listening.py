import os
import pyrebase
import predict, train_svm_classifier
from sklearn.externals import joblib
from keras.models import load_model
import numpy as np


config = {
  "apiKey": "AIzaSyBDpF9R11deKSYnlPZwkgtPQKwe2bnfXkY",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://obss-hackathon.firebaseio.com",
  "storageBucket": "obss-hackathon.appspot.com"
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()
db = firebase.database()


def url_stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    file_name = 'image.jpg'
    storage.child("images" + message["path"]).download(file_name)

    ## process image
    id_ = predict.predict(load_model('./models/conv_model.h5'), joblib.load('./models/svm_model.pkl'), file_name)
    places = os.listdir('./data/train')
    out_file = os.path.join('./data/train', places[id_], 'default.jpg')

    # put to database
    db.child("result" + message["path"] + "result").set(str(id_) + '_default.jpg')
    # db.child("url" + message["path"]).set(None)


my_stream = db.child("url").stream(url_stream_handler)
