
import pyrebase

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
    image = storage.child("images" + message["path"]).download("downloaded.jpg")

    ## process image

    ##

    # put to database
    # TODO: Change put function to processed image name
    storage.child("images" + message["path"] + "result").put("downloaded.jpg")
    db.child("result" + message["path"] + "result").set(True)

my_stream = db.child("url").stream(stream_handler)
