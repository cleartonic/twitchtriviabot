from src.connection import Connection
from src.commander import Commander
import time

class Trivvy:

    def __init__(self, connection, commander):
        self.connection = connection
        self.scan = connection.scan
        self.message_rate = connection.seconds_per_message
        self.router = commander

    def run(self):
        while self.connection.keep_IRC_running:
            new_chat_message = self.scan()
            self.router.respond_to(new_chat_message)
            time.sleep(self.message_rate)
