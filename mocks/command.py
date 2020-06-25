import time
from mocks.connection import Connection

class Spy_Command():

    def __init__(self):
        self._history = []

    def ping(self, _connection, message):
        self._history.append(message)

    def long_run(self, _connection, message):
        self.ping(_connection, message)
        time.sleep(Connection.seconds_per_message * 25)
        self.ping(_connection, (message[1], "completed"))
