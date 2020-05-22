class Connection:

    def __init__(self):
        self._message = 'No message recieved.'

    def send(self, message):
        self._message = message
