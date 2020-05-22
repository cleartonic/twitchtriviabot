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

    def test_round_lets_the_chat_know_a_new_round_started_by_sending_its_name(self):
        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        mock_connection = Connection()
        s = Subject(Questioner, questions, mock_connection, Players())
        s.start()
        self.assertTrue("2" in mock_connection._message)

    def test_round_lets_the_chat_know_when_the_round_is_over_by_listing_round_winners(self):
        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        mock_connection = Connection()
        mock_players = Players()
        gold = f"{mock_players._round_winners[0][0]}: {mock_players._round_winners[0][1]}"
        silver = f"{mock_players._round_winners[1][0]}: {mock_players._round_winners[1][1]}"
        bronze = f"{mock_players._round_winners[2][0]}: {mock_players._round_winners[2][1]}"

        s = Subject(Questioner, questions, mock_connection, mock_players)
        s.go()

        self.assertTrue(gold in mock_connection._message)
        self.assertTrue(silver in mock_connection._message)
        self.assertTrue(bronze in mock_connection._message)
