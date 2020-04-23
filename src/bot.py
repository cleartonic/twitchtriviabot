from src.connection_vars import Connection
from src.game_vars import Game
from src.scanner import scanloop
import time

class Trivvy:

    def __init__(self, scanner):
        self.scanloop = scanner

    def run(self):
        while Connection.keep_IRC_running:
            if Game.trivia_active:
                trivia_routinechecks()
            self.scanloop()
            time.sleep(1 / Connection.RATE)
