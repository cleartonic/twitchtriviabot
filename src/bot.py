from src.connection import Connection
from src.game import Game
import time

class Trivvy:

    def __init__(self, connection):
        self.conn = connection
        self.scan = connection.scan
        self.message_rate = connection.seconds_per_message

    def run(self):
        while self.conn.keep_IRC_running:
            reply = self.scan()
            if Game.trivia_active:
                trivia_routinechecks(reply)
            time.sleep(self.message_rate)
