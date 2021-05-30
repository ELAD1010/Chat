class Message(object):
    """
    This class purpose is to create an object from type Message.
    """
    def __init__(self, msg_type, sender):
        self.msg_type = msg_type
        self.sender = sender

    def get_type(self):
        return self.msg_type

    def get_sender(self):
        return self.sender


class BroadcastMessage(Message):
    def __init__(self, type, sender, receiver, data):
        super(BroadcastMessage, self).__init__(type, sender)
        self.receiver = receiver
        self.data = data

    def get_receiver(self):
        return self.receiver

    def get_data(self):
        return self.data

    def show_msg(self, username):
        if self.sender == username:
            return 'Me: ' + self.data
        else:
            return self.sender + ': ' + self.data

class UnicastMessage(Message):
    def __init__(self, type, sender, receiver, data):
        super(UnicastMessage, self).__init__(type, sender)
        self.receiver = receiver
        self.data = data

    def get_receiver(self):
        return self.receiver

    def get_data(self):
        return self.data

    def show_msg(self, username):
        if self.sender == username:
            return 'Me to {receiver}: {data}'.format(receiver=self.receiver, data=self.data)
        else:
            return 'From {sender}: {data}'.format(sender=self.sender, data=self.data)

class LoginMessage(Message):
    def __init__(self,msg_type, sender, username, password):
        super(LoginMessage, self).__init__(msg_type, sender)
        self.username = username
        self.password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

