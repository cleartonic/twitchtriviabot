class Connection:

    def __init__(self):
        self._message = 'No message recieved.'
        self._message_list = []
        self.last_response = ('bot', 'No Messages Recieved')
        self.seconds_per_message = 1 / 100000

    def send(self, message):
        self._message_list.append(message)
        self._message = message
