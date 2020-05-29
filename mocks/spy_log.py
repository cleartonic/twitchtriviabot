class Spy_Log:

    def __init__(self):
        self._history = []

    def log(self, message):
        self._history.append(message)

    def clear(self):
        self._history = []
