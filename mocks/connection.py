class Connection:

    def __init__(self):
        self.message = 'No message recieved.'

    def send(self, message):
        self.message = message
