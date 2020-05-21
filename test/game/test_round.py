import unittest
from mocks.connection import Connection
from mocks.game_record import Game_Record
from mocks.players import Players
from src.messages import Chat
from src.game.questioner import Questioner
from src.game.round import Round as Subject

class RoundTestCase(unittest.TestCase):
    def test_round_organizes_questions_for_a_questioner(self):
        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        subject = Subject(Questioner, questions, Connection(), Players())
        self.assertEqual(subject.questioners[0].ask, 'What is your name?')
        self.assertEqual(subject.questioners[1].ask, 'What is your quest?')
        self.assertEqual(subject.questioners[2].ask, 'What is your favorite color?')

    def test_round_lets_the_chat_know_a_new_round_started(self):
        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        mock_connection = Connection()
        s = Subject(Questioner, questions, mock_connection, Players())
        s.start()
        self.assertEqual(mock_connection.message, Chat.new_round)

    def test_round_lets_the_chat_know_when_the_round_is_over(self):
        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        mock_connection = Connection()
        s = Subject(Questioner, questions, mock_connection, Players())
        s.go()
        self.assertEqual(mock_connection.message, Chat.end_round)
