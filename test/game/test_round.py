import unittest
from mocks.connection import Connection
from mocks.game_record import Game_Record
from src.game.questioner import Questioner
from src.game.round import Round as Subject

class RoundTestCase(unittest.TestCase):
    def test_round_organizes_questions_for_a_questioner(self):
        any_answer_is_right = True

        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        subject = Subject(Questioner, questions, Connection())
        self.assertEqual(subject.questioners[0].ask, 'What is your name?')
        self.assertEqual(subject.questioners[1].ask, 'What is your quest?')
        self.assertEqual(subject.questioners[2].ask, 'What is your favorite color?')
