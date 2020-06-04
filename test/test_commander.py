import unittest
from mocks.connection import Connection
from mocks.silent_log import dont_print
from src.commander import Commander as Subject

class CommanderTestCase(unittest.TestCase):
    def test_commander_initializes_with_no_messages_recieved(self):
        no_admins = []
        mock_connection = Connection
        s = Subject(no_admins, mock_connection, dont_print)
        self.assertEqual(s.last_response, ('bot', 'No Messages Recieved'))
