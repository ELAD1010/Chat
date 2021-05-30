import threading, json
from tkinter import *
from tkinter import filedialog, messagebox
from io import BytesIO

from PIL import ImageTk, Image
import requests
import os
import urllib
from functools import partial

from messages import *
#from firebaseManager import Firebase
WINDOW_WIDTH = 700


class ChatScreen():

    def __init__(self, user, socket):
        self.chat_window = Tk()
        self.user = user
        self.client = socket
        self.scroll = Scrollbar(self.chat_window, activebackground='Blue')
        self.msg_entry = Entry(self.chat_window, width=50)
        self.messages = Text(self.chat_window, yscrollcommand=self.scroll.set, width= 70)
        self.user_list = Listbox(self.chat_window, width=20, height = 10, font=('Times', 18))
        self.panel = ""
        self.img = ""
        self.lines = 0
        self.build()
        self.y = 95
        self.photos = []
        self.user_panels = []

    def run(self):
        self.chat_window.mainloop()

    def build(self):
        self.chat_window.title('Chat')
        self.chat_window.geometry('900x500+500+300')
        self.chat_window.protocol('WM_DELETE_WINDOW', self.exit_chat)
        add_img_bt = Button(self.chat_window, width=20, text="Add Profile Image", fg="black", command=self.add_profile_pic)
        add_img_bt.place(x= 210, y= 20)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.messages.place(x=20, y=60)
        self.scroll.configure(command=self.messages.yview)
        self.msg_entry.place(x=140, y=470)
        #img_link = Firebase.retrieve_img_from_firebase(self.user.get("username"))
        img_link = "https://images.pexels.com/photos/3680219/pexels-photo-3680219.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
        response = requests.get(img_link)
        img_data = response.content
        image = Image.open(BytesIO(img_data))
        image = image.resize((48, 48), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.panel = Label(self.chat_window, image=self.img)
        self.panel.place(x= 450, y=6)
        send_bt = Button(self.chat_window, width=12, text='Send Broadcast', fg='white', bg='#DB06F4', command= self.send_broadcast)
        send_bt.place(x=500, y=445)
        send_bt2 = Button(self.chat_window, width=12, text="Send Private", fg="Blue", bg='Green', command = self.send_private)
        send_bt2.place(x=500, y= 470)
        lbl1 = Label(self.chat_window, text="Online Users", font=18)
        lbl1.place(x=705, y=60)
        self.user_list.place(x=620, y=95)
        name_lbl = Label(self.chat_window, text=self.user.get("username"), font=18)
        name_lbl.place(x=510, y=12)

    def add_profile_pic(self):
        file_path = filedialog.askopenfilename()
        print (file_path)
        if file_path != "":
            Firebase.upload_img_to_firebase(file_path, self.user.get("username"))
            self.refresh_profile_pic()
            self.client.send("update_photos\n".encode())


    def send_broadcast(self):
        msg = self.msg_entry.get()
        uname = self.user.get("username")
        if msg != '':
            message = BroadcastMessage("Broadcast", uname, "broadcast", msg)
            self.send(message)
            self.messages.insert(INSERT, message.show_msg(self.user.get("username")) + '\n')
            self.lines += 1
            self.messages.tag_add("my_msg", str(self.lines) + '.0', str(self.lines) + '.' + str(len(message.show_msg(uname))))
            self.messages.tag_config("my_msg", foreground='Blue')
            self.msg_entry.delete(0, "end")

    def send(self, message):
        json_msg = {"msgType": message.get_type(), "sender": message.get_sender(),
                    "receiver": message.get_receiver(),
                    "data": message.get_data()}

        self.client.send((json.dumps(json_msg) + '\n').encode())

    def send_private(self):
        index = self.user_list.curselection()
        if len(index) == 0:
            messagebox.showwarning("Private Message Warning", "Please select a participant from online users list")
        else:
            dest_username = self.user_list.get(index)
            msg = self.msg_entry.get()
            username = self.user.get("username")
            if msg != '':
                message = UnicastMessage("Unicast", username, dest_username, msg)
                self.send(message)
                self.messages.insert(INSERT, message.show_msg(self.user.get("username")) + '\n')
                self.lines += 1
                self.messages.tag_add("my_msg", str(self.lines) + '.0', str(self.lines) + '.' + str(len(message.show_msg(username))))
                self.messages.tag_config("my_msg", foreground='Blue')
                self.msg_entry.delete(0, "end")

    def exit_chat(self):
        self.client.send("Offline\n".encode())
        self.client.close()
        self.chat_window.destroy()

    def refresh_profile_pic(self):
        img_link = Firebase.retrieve_img_from_firebase(self.user.get("username"))
        response = requests.get(img_link)
        img_data = response.content
        image = Image.open(BytesIO(img_data))
        image = image.resize((48, 48), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        self.panel.config(image=img)
        self.panel.photo_ref = img



    def display_message(self, msg):
        self.messages.insert(INSERT, msg.show_msg(self.user.get("username")) + '\n')
        self.lines += 1


    def displayList(self, users):
        self.resetScreen()
        for user in users:
            if user != self.user:
                self.user_list.insert(END, user)
                img_link = Firebase.retrieve_img_from_firebase(user)
                response = requests.get(img_link)
                img_data = response.content
                image = Image.open(BytesIO(img_data))
                image = image.resize((26, 26), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image)
                self.photos.append(img)
                panel = Label(self.chat_window, image=img)
                panel.place(x=680, y=self.y)
                self.user_panels.append(panel)
                self.y += 30

    def resetScreen(self):
        print(self.user_panels)
        self.user_list.delete(0, END)
        for panel in self.user_panels:
            panel.config(image='')
        self.photos = []
        self.user_panels = []
        self.y = 95



