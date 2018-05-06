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


def train_stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    file_name = 'image.jpg'
    storage.child("images" + message["path"]).download(file_name)

    id_ = list(message["data"].keys())[0]
    print(id_)
    ## process image
    embedding_model = load_model('./models/conv_model.h5')

    x_train_svm = np.load('./x_train_svm.npy')
    x_train_svm = np.vstack([x_train_svm, predict.extract_embedding(embedding_model, file_name)])

    y_train_svm = np.load('./y_train_svm.npy')
    y_train_svm = np.hstack([y_train_svm, int(id_)])

    np.save('./x_train_svm.npy', x_train_svm)
    np.save('./y_train_svm.npy', y_train_svm)
    
    train_svm_classifier.train_svm()

    # db.child("training" + message["path"]).set(None)


my_stream = db.child("training").stream(train_stream_handler)
