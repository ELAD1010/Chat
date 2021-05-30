import json
import socket
from tkinter import *
from tkinter import messagebox

from messages import LoginMessage
from client import Client

HOST = '127.0.0.1'
PORT = 8001

class RegisterScreen:
    def __init__(self, login_screen):
        self.register = Tk()
        self.register.withdraw()
        self.login_screen = login_screen
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.uname = ""
        self.password = ""
        self.user = {}
        self.user_entry = Entry(self.register, width=25)
        self.password_entry = Entry(self.register, show='*', width=25)
        self.password_check_entry = Entry(self.register, show='*', width=25)
        self.build()

    def show(self):
        self.register.deiconify()
        self.login_screen.withdraw()

    def hide(self):
        self.register.withdraw()
        self.login_screen.deiconify()

    def build(self):
        self.register.title('Register')
        self.register.geometry('400x200+680+390')
        self.register.protocol('WM_DELETE_WINDOW', self.exit_on_register_menu)
        user_text = Label(self.register, text="Username:")
        user_text.pack(expand=0)
        self.user_entry.pack(expand=0)
        password_text = Label(self.register, text="Password:")
        password_text.pack(expand=0)
        self.password_entry.pack(expand=0)
        password_check_text = Label(self.register, text="Re Enter Password:")
        password_check_text.pack(expand=0)
        self.password_check_entry.pack(expand=0)
        user_enter_bt = Button(self.register, text='Enter', fg='Blue', command=self.user_register)
        user_enter_bt.pack(expand=0)
        user_enter_bt = Button(self.register, text='Clear', fg='Blue', width=20, command=self.clear)
        user_enter_bt.pack(expand=0)
        back_to_login_bt = Button(self.register, text="Back To Login", width=20, command= self.hide)
        back_to_login_bt.pack(expand=0)

    def check_username(self):
        if self.uname == "":
            return False
        return True

    def check_password(self):
        retval = True
        if self.password != self.password_check_entry.get():
            messagebox.showerror("Error", "Different passwords!")
            retval = False
        return retval

    def exit_on_register_menu(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()
            exit()

    def clear(self):
        self.user_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.password_check_entry.delete(0, END)

    def user_register(self):
        self.uname = self.user_entry.get()
        self.password = self.password_entry.get()
        if self.check_password() and self.check_username():
            if not self.check_user_exists():
                self.destroy()
                client = Client(self.user, self.socket)
                client.start()
            else:
                messagebox.showerror("Error", "Username already exists")

    def destroy(self):
        self.register.destroy()
        self.login_screen.destroy()

    def check_user_exists(self):
        self.socket.connect((HOST, PORT))
        user_exist = False
        user_info = LoginMessage("Register", self.uname, self.uname, self.password)
        self.user = {"msg_type": user_info.get_type(), "sender": user_info.get_sender(),
                "username": user_info.get_username(),
                "password": user_info.get_password()}
        print(json.dumps(self.user))
        self.socket.send((json.dumps(self.user) + '\n').encode())
        acceptance_msg = self.socket.recv(1024).decode()
        acceptance_msg = acceptance_msg[0:acceptance_msg.find('\r')]
        if acceptance_msg == "Exists":
            user_exist = True
            self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        return user_exist
