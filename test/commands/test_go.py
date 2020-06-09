import unittest
from mocks.connection import Connection
from mocks.game.game_record import Game_Record
from mocks.game.players import Players
from mocks.silent_log import dont_print
from mocks.spy_log import Spy_Log
from src.messages.terminal import Log
from src.commands import Go

class GoCommandTestCase(unittest.TestCase):
    def test_tuple_returns_the_configured_command_tuple(self):
        subject = Go("mocks/triviaset.csv", Game_Record(), Players())
        command = subject.tuple()
        self.assertEqual(command[0], "!go")
        self.assertEqual(command[1], subject.run_the_next_trivia_round)
        self.assertEqual(command[2], [ "admin_only" ])

    def test_run_the_next_trivia_round_runs_a_whole_round(self):
        mock_players = Players()
        s = Go("mocks/triviaset.csv", Game_Record(), mock_players)

        mock_connection = Connection()
        _message = "irrelevant in this instance"
        s.run_the_next_trivia_round(mock_connection, _message)

        winner = mock_players._round_winners[0][0]
        self.assertTrue(winner in mock_connection._message)

    def test_skips_running_the_next_trivia_round_if_theres_an_error(self):
        s = Go("mocks/bad_triviaset.csv", Game_Record(), Players(), dont_print)

        mock_connection = Connection()
        _message = "irrelevant in this instance"
        s.run_the_next_trivia_round(mock_connection, _message)

        self.assertEqual(mock_connection._message, 'No message recieved.')

    def test_logs_if_theres_an_error(self):
        spy = Spy_Log()
        s = Go("mocks/bad_triviaset.csv", Game_Record(), Players(), spy.log)

        mock_connection = Connection()
        _message = "irrelevant in this instance"
        s.run_the_next_trivia_round(mock_connection, _message)

        self.assertTrue("Ask" in spy._history[-1] and "4" in spy._history[-1])
