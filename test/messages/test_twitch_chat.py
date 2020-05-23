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

    def test_chat_new_game_message_not_too_long(self):
        players = [
            ("ABCDEFGHIJKLMNOPQRSTUVWXY", 5000),
            ("UserNameThats25characters", 4000),
            ("leutenant_junior_grade_bo", 3000)
        ]
        actual = Subject.new_game(players)
        self.assertLessEqual(len(actual), 255)

    def test_chat_includes_an_end_game_signoff_for_end_games(self):
        players = [
            ("GoldPlayer", 5),
            ("SilverPlayer", 4),
            ("BronzePlayer", 3)
        ]
        actual = Subject.end_game(players)
        signoff_included = False
        for option in Subject.end_game_signoff:
            if option in actual:
                signoff_included = True
        self.assertTrue(signoff_included)

    def test_chat_end_game_message_not_too_long(self):
        players = [
            ("ABCDEFGHIJKLMNOPQRSTUVWXY", 5000),
            ("UserNameThats25characters", 4000),
            ("leutenant_junior_grade_bo", 3000)
        ]
        actual = Subject.end_game(players)
        self.assertLessEqual(len(actual), 255)

    def test_chat_includes_an_end_of_round_signoff_for_end_rounds(self):
        players = [
            ("GoldPlayer", 5),
            ("SilverPlayer", 4),
            ("BronzePlayer", 3)
        ]
        actual = Subject.end_round(players)
        conclusion_included = False
        for option in Subject.end_round_conclusion:
            if option in actual:
                conclusion_included = True
        self.assertTrue(conclusion_included)

    def test_chat_end_round_message_not_too_long(self):
        players = [
            ("ABCDEFGHIJKLMNOPQRSTUVWXY", 5000),
            ("UserNameThats25characters", 4000),
            ("leutenant_junior_grade_bo", 3000)
        ]
        actual = Subject.end_round(players)
        self.assertLessEqual(len(actual), 255)
