import unittest
import time
from concurrent.futures import ThreadPoolExecutor
from mocks.connection import Connection
from mocks.game.game_record import Game_Record
from mocks.game.players import Players
from src.messages import Chat
from src.game.round import Round as Subject

class RoundTestCase(unittest.TestCase):
    def test_round_organizes_questions_for_a_questioner(self):
        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        subject = Subject(questions, Connection(), Game_Record(), Players())
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
        s = Subject(questions, mock_connection, Game_Record(), Players())
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

        s = Subject(questions, mock_connection, Game_Record(), mock_players)
        s.go()

        self.assertTrue(gold in mock_connection._message)
        self.assertTrue(silver in mock_connection._message)
        self.assertTrue(bronze in mock_connection._message)

    def test_round_tells_players_to_reset_scores_for_a_new_round_at_the_end_of_its_go(self):
        questions = [
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
        ]
        mock_players = Players()
        s = Subject(questions, Connection(), Game_Record(), mock_players)
        s.end()
        self.assertEqual(mock_players._next_round_called, "Round Scores Reset")

    def chat(self, connection, response):
        connection.last_response = response
        time.sleep(connection.seconds_per_message)

    def failure(self, connection):
        self.chat(connection, ("VILLAGER_1", "Bread!"))
        self.chat(connection, ("VILLAGER_2", "Apples!"))
        self.chat(connection, ("VILLAGER_3", "Very small rocks!"))
        self.chat(connection, ("VILLAGER_1", "Cider!"))
        self.chat(connection, ("VILLAGER_2", "Uhhh, gravy!"))
        self.chat(connection, ("VILLAGER_1", "Cherries!"))
        self.chat(connection, ("VILLAGER_2", "Mud!"))
        self.chat(connection, ("VILLAGER_3", "Churches -- churches!"))
        self.chat(connection, ("VILLAGER_2", "Lead -- lead!"))

    def success(self, connection):
        self.failure(connection)
        self.chat(connection, ("Arthur", "A duck."))
        self.chat(connection, ("knight_who_says_ni", "Ni!"))

    def chat_thread(self, connection):
        self.success(connection)
        self.failure(connection)

    def test_round_runs_through_a_tiny_round_flow_example(self):
        questions = [{
            'Round': 1,
            'Ask': "What also floats in water?",
            'Answer': "A Duck!"
        },
        {
            'Round': 1,
            'Ask': "What is the average airspeed velocity of an unladen swallow?",
            'Answer': "What do you mean? African or European?"
        }]
        mock_connection = Connection()
        mock_players = Players()
        s = Subject(questions, mock_connection, Game_Record(), mock_players)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.go)
            e.submit(self.chat_thread, mock_connection)
            
        self.assertTrue("1" in mock_connection._message_list[0])
        self.assertEqual(questions[0]["Ask"], mock_connection._message_list[1])
        self.assertTrue(questions[1]["Ask"] in mock_connection._message_list)
        self.assertTrue(mock_players._round_winners[0][0] in mock_connection._message)
