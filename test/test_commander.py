import unittest
from mocks.connection import Connection
from mocks.socket import socket
from mocks.time import Time
from mocks.silent_log import dont_print
from mocks.spy_log import Spy_Log
from src.commander import Commander as Subject

class CommanderTestCase(unittest.TestCase):
    def test_commander_initializes_with_no_messages_recieved(self):
        no_admins = []
        s = Subject(no_admins, Connection(), dont_print)
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

    def test_commander_initializes_with_no_messages_recieved(self):
        test_response = ("gandhi", "Be the change you want to see in the world.")
        no_admins = []
        mock_connection = Connection()
        mock_time = Time(dont_print).sleep
        s = Subject(no_admins, mock_connection, dont_print, mock_time)

        mock_connection.last_response = test_response
        s.check_connection_last_message()

        self.assertEqual(s.last_response, test_response)
