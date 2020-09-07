import unittest
import os
from src.game.game_record import Game_Record as Subject

class Game_Record_TestCase(unittest.TestCase):
    def cleanup(self, filename):
        if os.path.exists(f"{filename}.txt"):
            os.remove(f"{filename}.txt")

    def skip_test_game_record_log_creates_a_log_with_a_single_entry_upon_creation(self):
        pass

    def skip_test_game_record_log_updates_the_log_with_a_new_entry(self):
        pass

    def skip_test_game_record_clear_game_replaces_the_log_with_an_empty_list(self):
        pass

    def skip_test_game_record_log_returns_the_current_logged_questions(self):
        pass