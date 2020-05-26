class Connection:

    def __init__(self):
        self._message = 'No message recieved.'
        self.last_response = ('bot', 'No Messages Recieved')

    def send(self, message):
        self._message = message
