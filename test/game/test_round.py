import unittest
from mocks.game.questioner import Questioner
mock = Questioner.mock
from src.game.round import Round as Subject

class RoundTestCase(unittest.TestCase):
    def test_round_organizes_questions_for_a_questioner(self):
        any_answer_is_right = True
        questioner = mock(any_answer_is_right)
        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        Subject(questioner, questions)
