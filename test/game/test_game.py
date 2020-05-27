import unittest
from mocks.connection import Connection
from mocks.game.game_record import Game_Record
from mocks.game.players import Players
from src.messages import Chat
from src.game.round import Round
from src.game.questioner import Questioner
from src.game.game import Game as Subject

class GameTestCase(unittest.TestCase):
    def test_game_organizes_questions_into_rounds_for_each_round_instance(self):
        questions = [
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 3, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        subject = Subject(Round, Questioner, questions, Connection(), Game_Record(), Players())
        self.assertEqual(subject.rounds[0].questioners[0].ask, "What's a Diorama?")
        self.assertEqual(subject.rounds[1].questioners[0].ask, 'What is your name?')
        self.assertEqual(subject.rounds[1].questioners[1].ask, 'What is your quest?')
        self.assertEqual(subject.rounds[1].questioners[2].ask, 'What is your favorite color?')
        self.assertEqual(subject.rounds[2].questioners[0].ask, 'Are you a god?')

    def test_game_lets_the_chat_know_a_new_game_started_with_who_the_greatest_players_are(self):
        questions = [
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 3, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        mock_connection = Connection()
        mock_players = Players()
        gold = f"{mock_players._top_players[0][0]}: {mock_players._top_players[0][1]}"
        silver = f"{mock_players._top_players[1][0]}: {mock_players._top_players[1][1]}"
        bronze = f"{mock_players._top_players[2][0]}: {mock_players._top_players[2][1]}"

        s = Subject(Round, Questioner, questions, mock_connection, Game_Record(), mock_players)
        s.start()

        self.assertTrue(gold in mock_connection._message)
        self.assertTrue(silver in mock_connection._message)
        self.assertTrue(bronze in mock_connection._message)

    def test_game_lets_the_chat_know_the_game_is_over_with_who_won(self):
        questions = [
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 3, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        mock_connection = Connection()
        mock_players = Players()
        gold = f"{mock_players._game_winners[0][0]}: {mock_players._game_winners[0][1]}"
        silver = f"{mock_players._game_winners[1][0]}: {mock_players._game_winners[1][1]}"
        bronze = f"{mock_players._game_winners[2][0]}: {mock_players._game_winners[2][1]}"

        s = Subject(Round, Questioner, questions, mock_connection, Game_Record(), mock_players)
        s.go()

        self.assertTrue(gold in mock_connection._message)
        self.assertTrue(silver in mock_connection._message)
        self.assertTrue(bronze in mock_connection._message)

    def test_game_clears_logs_if_it_reaches_the_end_of_the_game(self):
        questions = [
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 3, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        mock_game_record = Game_Record()
        s = Subject(Round, Questioner, questions, Connection(), mock_game_record, Players())
        s.end()
        self.assertEqual(mock_game_record._clear_received, True)

    def test_game_tells_players_to_score_game_winners_at_the_end_of_the_game(self):
        questions = [
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 3, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        mock_players = Players()
        s = Subject(Round, Questioner, questions, Connection(), Game_Record(), mock_players)
        s.end()
        self.assertEqual(mock_players._winner, mock_players._game_winners[0][0])

    def test_game_tells_players_to_reset_scores_for_a_new_game_at_the_end_of_the_game(self):
        questions = [
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 3, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        mock_players = Players()
        s = Subject(Round, Questioner, questions, Connection(), Game_Record(), mock_players)
        s.end()
        self.assertEqual(mock_players._next_game_called, "Game Scores Reset")

    def test_game_converts_a_flat_question_list_to_rounds(self):
        initial_questions = [
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 3, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        expected_questions = [
            [
                {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"}
            ],
            [
                {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
                {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
                {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'}
            ],
            [
                {'Round': 3, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
            ],
        ]
        mock_game_record = Game_Record()
        s = Subject(Round, Questioner, initial_questions, Connection(), mock_game_record, Players())
        actual_questions = s.list_by_rounds(initial_questions)
        self.assertEqual(actual_questions, expected_questions)

    def test_game_list_by_rounds_doesnt_care_about_sparse_sequences(self):
        initial_questions = [
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 5, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        expected_questions = [
            [
                {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"}
            ],
            [
                {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
                {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
                {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'}
            ],
            [
                {'Round': 5, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
            ],
        ]
        mock_game_record = Game_Record()
        s = Subject(Round, Questioner, initial_questions, Connection(), mock_game_record, Players())
        actual_questions = s.list_by_rounds(initial_questions)
        self.assertEqual(actual_questions, expected_questions)

    def test_game_list_by_rounds_doesnt_care_about_rounds_with_names(self):
        initial_questions = [
            {'Round': "Simpsons", 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': "Grail", 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': "Grail", 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
            {'Round': "Grail", 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': "Ghost", 'Ask': 'Are you a god?', 'Answer': 'YES!'}
        ]
        expected_questions = [
            [
                {'Round': "Simpsons", 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"}
            ],
            [
                {'Round': "Grail", 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
                {'Round': "Grail", 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'},
                {'Round': "Grail", 'Ask': 'What is your favorite color?', 'Answer': 'Blue'}
            ],
            [
                {'Round': "Ghost", 'Ask': 'Are you a god?', 'Answer': 'YES!'}
            ],
        ]
        mock_game_record = Game_Record()
        s = Subject(Round, Questioner, initial_questions, Connection(), mock_game_record, Players())
        actual_questions = s.list_by_rounds(initial_questions)
        self.assertEqual(actual_questions, expected_questions)

    def test_game_list_by_rounds_groups_rounds_by_when_they_appear_in_the_list(self):
        initial_questions = [
            {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
            {'Round': 5, 'Ask': 'Are you a god?', 'Answer': 'YES!'},
            {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
            {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"},
            {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'}
        ]
        expected_questions = [
            [
                {'Round': 2, 'Ask': 'What is your favorite color?', 'Answer': 'Blue'},
                {'Round': 2, 'Ask': 'What is your name?', 'Answer': 'Sir Lancelot of Camelot'},
                {'Round': 2, 'Ask': 'What is your quest?', 'Answer': 'To seek the Holy Grail'}
            ],
            [
                {'Round': 5, 'Ask': 'Are you a god?', 'Answer': 'YES!'}
            ],
            [
                {'Round': 1, 'Ask': "What's a Diorama?", 'Answer': "OMG Han! Chewie! They're all here!"}
            ]
        ]
        mock_game_record = Game_Record()
        s = Subject(Round, Questioner, initial_questions, Connection(), mock_game_record, Players())
        actual_questions = s.list_by_rounds(initial_questions)
        self.assertEqual(actual_questions, expected_questions)

    def test_game_init_rounds_returns_an_empty_array_if_no_questions_are_given(self):
        initial_questions = []
        mock_game_record = Game_Record()
        s = Subject(Round, Questioner, initial_questions, Connection(), mock_game_record, Players())
        actual_questions = s.init_rounds(initial_questions)
        self.assertEqual(actual_questions, initial_questions)
