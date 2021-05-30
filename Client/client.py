from tkinter import messagebox, filedialog
from tkinter import *
from PIL import ImageTk, Image
import urllib
import socket, json
import os

from messages import *
from firebaseManager import *


from chatScreen import *
import threading

WINDOW_WIDTH = 700
LEN_OF_LENGTH = 5
HOST = '127.0.0.1'
PORT = 8001


class Client(threading.Thread):
    def __init__(self, user, cli_sock):
        threading.Thread.__init__(self)
        self.socket = cli_sock
        self.user = user
        self.isAlive = True
        self.chatScreen = ""

    def receive(self):
        while self.isAlive:
            data = self.socket.recv(2048).decode()
            print(data)
            if data == '':
                break
            print(data)
            msg_dict = json.loads(data)
            self.check_type(msg_dict, msg_dict.get("msgType"))

    def run(self):
        print("hello")
        self.chatScreen = ChatScreen(self.user, self.socket)
        self.receive_thread = threading.Thread(target=self.receive, args=())
        self.receive_thread.start()
        self.chatScreen.run()

    def send(self):
        self.socket.send("Online\n".encode())

    def check_type(self, msg_dict, type):
        if type == "Broadcast":
            msg = BroadcastMessage(msg_dict.get("msgType"), msg_dict.get("sender"), msg_dict.get("receiver"),
                                   msg_dict.get("data"))
            self.chatScreen.display_message(msg)
        elif type == "Unicast":
            msg = UnicastMessage(msg_dict.get("msgType"), msg_dict.get("sender"), msg_dict.get("receiver"),
                                   msg_dict.get("data"))
            self.chatScreen.display_message(msg)
        elif type == "Users":
            self.chatScreen.displayList(msg_dict.get('data'))









