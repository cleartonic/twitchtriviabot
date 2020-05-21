import unittest
from src.messages import Chat as Subject

class TwitchChatTestCase(unittest.TestCase):
    def test_chat_includes_a_new_game_catchprase_for_new_games(self):
        players = [
            ("GoldPlayer", 5),
            ("SilverPlayer", 4),
            ("BronzePlayer", 3),
            ("CopperPlayer", 2),
            ("IronPlayer", 1)
        ]
        actual = Subject.new_game(players)
        catchphrase_included = False
        for option in Subject.new_game_catchphrase:
            if option in actual:
                catchphrase_included = True
        self.assertTrue(catchphrase_included)

    def test_chat_includes_an_end_game_signoff_for_end_games(self):
        players = [
            ("GoldPlayer", 5),
            ("SilverPlayer", 4),
            ("BronzePlayer", 3),
            ("CopperPlayer", 2),
            ("IronPlayer", 1)
        ]
        actual = Subject.end_game(players)
        signoff_included = False
        for option in Subject.end_game_signoff:
            if option in actual:
                signoff_included = True
        self.assertTrue(signoff_included)

    def test_chat_includes_an_end_of_round_signoff_for_end_rounds(self):
        players = [
            ("GoldPlayer", 5),
            ("SilverPlayer", 4),
            ("BronzePlayer", 3),
            ("CopperPlayer", 2),
            ("IronPlayer", 1)
        ]
        actual = Subject.end_round(players)
        conclusion_included = False
        for option in Subject.end_round_conclusion:
            if option in actual:
                conclusion_included = True
        self.assertTrue(conclusion_included)
