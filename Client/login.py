
from loginScreen import *


class Login(threading.Thread):
    def __int__(self):
        threading.Thread.__init__(self)

    def run(self):
        loginScreen = LoginScreen()
        loginScreen.run()

