
from client import *
from registerScreen import *


HOST = '127.0.0.1'
PORT = 8001

class LoginScreen:
    def __init__(self):
        self.user_box = Tk()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_exit = False
        self.uname = ""
        self.password = ""
        self.user_clicked = False
        self.user_entry = Entry(self.user_box, width=25)
        self.password_entry = Entry(self.user_box, show='*', width=25)
        self.build()
        self.registerScreen = RegisterScreen(self.user_box)
        self.run()

    def run(self):
        self.user_box.mainloop()


    def build(self):
        self.user_box.title('Login')
        self.user_box.geometry('400x200+680+390')
        self.user_box.protocol('WM_DELETE_WINDOW', self.exit_on_login_menu)
        user_text = Label(self.user_box, text="Username:")
        user_text.pack(expand=0)
        self.user_entry.pack(expand=0)
        password_text = Label(self.user_box, text="Password:")
        password_text.pack(expand=0)
        self.password_entry.pack(expand=0)
        user_enter_bt = Button(self.user_box, text='Enter', fg='Blue', command=self.user_login)
        user_enter_bt.pack(expand=0)
        user_register_bt = Button(self.user_box, text='Register', fg="Blue", command=self.open_register)
        user_register_bt.pack(expand=0)

    def open_register(self):
        self.registerScreen.show()

    def exit_on_login_menu(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()
            exit()

    def destroy(self):
        self.user_box.destroy()

    def user_login(self):
        self.uname = self.user_entry.get()
        self.password = self.password_entry.get()
        self.socket.connect((HOST, PORT))
        user_info = LoginMessage("Login", self.uname, self.uname, self.password)
        user = {"msg_type": user_info.get_type(), "sender": user_info.get_sender(),
                "username": user_info.get_username(),
                "password": user_info.get_password()}
        print(json.dumps(user))
        self.socket.send(
            (json.dumps(user) + '\n').encode())  # Sending username and password in order to connect to the server.
        acceptance_msg = self.socket.recv(1024).decode()
        acceptance_msg = acceptance_msg[0:acceptance_msg.find('\r')]
        if acceptance_msg == 'Incorrect':
            messagebox.showwarning('Failed To Login', 'Password is incorrect!')
            self.socket.close()  # Close the socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create new socket in order to connect again.
        elif acceptance_msg == 'Already logged in':
            messagebox.showwarning('Failed To Login', 'The user has already logged in')
            self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create new socket in order to connect again.
        elif acceptance_msg == 'Correct':
            self.destroy()
            client = Client(user, self.socket)
            client.start()



