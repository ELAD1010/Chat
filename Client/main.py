
from login import Login
from firebaseManager import Firebase

HOST = '127.0.0.1'
PORT = 8001


Firebase.init_firebase()
login = Login()
login.start()
