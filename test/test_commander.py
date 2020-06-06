import unittest
from mocks.connection import Connection
from mocks.socket import socket
from mocks.time import Time
from mocks.silent_log import dont_print
from mocks.spy_log import Spy_Log
from src.messages import Log
from src.commander import Commander as Subject

class CommanderTestCase(unittest.TestCase):
    def test_commander_initializes_with_no_messages_recieved(self):
        s = Subject([], Connection(), dont_print)
        self.assertEqual(s.last_response, ('bot', 'No Messages Recieved'))

    def test_commander_case_insensitizes_admin_names(self):
        fancy_admins = [
            "dont_change_my_name",
            "PlEaSe_cHaNgE_Me",
            "!#@$_ni!_:="
        ]

        s = Subject(fancy_admins, Connection(), dont_print)

        self.assertEqual(s.admins[0], fancy_admins[0])
        self.assertEqual(s.admins[1], "please_change_me")
        self.assertEqual(s.admins[2], fancy_admins[2])

    def test_commander_remembers_the_last_new_message_from_Connection(self):
        no_admins = []
        test_response1 = ("gandhi", "Be the change you want to see in the world.")
        test_response2 = ("the_beatles", "Love is all you need.")
        mock_connection = Connection()
        dont_sleep = Time(dont_print).sleep
        s = Subject(no_admins, mock_connection, dont_print, dont_sleep)

        mock_connection.last_response = test_response1
        s.check_connection_last_message()

        self.assertEqual(s.last_response, test_response1)

        mock_connection.last_response = test_response2
        s.check_connection_last_message()

        self.assertEqual(s.last_response, test_response2)

    def test_commander_logs_when_a_non_admin_attempts_a_go_command(self):
        no_admins = []
        test_response = ("not_an_admin", "!go")
        expected_log = Log.bad_admin(test_response[0], test_response[1])
        mock_connection = Connection()
        spy = Spy_Log()
        dont_sleep = Time(dont_print).sleep
        s = Subject(no_admins, mock_connection, spy.log, dont_sleep)

        mock_connection.last_response = test_response
        s.check_connection_last_message()

        self.assertEqual(spy._history[-1], expected_log)

    def test_commander_logs_when_a_non_admin_attempts_a_stop_command(self):
        no_admins = []
        test_response = ("not_an_admin", "!stop")
        expected_log = Log.bad_admin(test_response[0], test_response[1])
        mock_connection = Connection()
        spy = Spy_Log()
        dont_sleep = Time(dont_print).sleep
        s = Subject(no_admins, mock_connection, spy.log, dont_sleep)

        mock_connection.last_response = test_response
        s.check_connection_last_message()

        self.assertEqual(spy._history[-1], expected_log)

    def test_commander_does_not_log_non_existent_commands(self):
        admins = ["admiral_akbar"]
        test_response = (admins[0], "!not_a_command")
        expected_log = Log.bad_admin(test_response[0], test_response[1])
        mock_connection = Connection()
        spy = Spy_Log()
        dont_sleep = Time(dont_print).sleep
        s = Subject(admins, mock_connection, spy.log, dont_sleep)

        mock_connection.last_response = test_response
        s.check_connection_last_message()

        self.assertEqual(len(spy._history), 0)
