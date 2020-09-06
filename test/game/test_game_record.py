import unittest
import os
from src.game.game_record import Game_Record as Subject

class Game_Record_TestCase(unittest.TestCase):
    def cleanup(self, filename):
        if os.path.exists(f"{filename}.txt"):
            os.remove(f"{filename}.txt")