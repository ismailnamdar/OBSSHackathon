import os
import pyrebase
from OBSSHackathon_ml.predict import predict

config = {
  "apiKey": "AIzaSyBDpF9R11deKSYnlPZwkgtPQKwe2bnfXkY",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://obss-hackathon.firebaseio.com",
  "storageBucket": "obss-hackathon.appspot.com"
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()
db = firebase.database()

def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    file_name = 'image.jpg'
    storage.child("images" + message["path"]).download(file_name)

    ## process image
    id_ = predict('./OBSSHackathon_ml/models/model.h5', file_name)
    places = os.listdir('./OBSSHackathon_ml/data/train')
    out_file = os.path.join('./OBSSHackathon_ml/data/train', places[id_], 'default.jpg')

    # put to database
    db.child("result" + message["path"] + "result").set(str(id_) + '_default.jpg')

my_stream = db.child("url").stream(stream_handler)
