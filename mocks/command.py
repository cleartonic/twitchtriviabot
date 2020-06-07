class Spy_Command():

    def __init__(self):
        self._history = []

    def ping(self, _connection, message):
        self._history.append(message)
