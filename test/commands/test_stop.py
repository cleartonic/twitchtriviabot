import unittest
from mocks.connection import Connection
from src.messages.twitch_chat import Chat
from src.commands import stop

class StopCommandTestCase(unittest.TestCase):
    def test_tuple_returns_the_configured_command_tuple(self):
        command = stop.tuple()

        self.assertEqual(command[0], "!stop")
        self.assertEqual(command[1], stop.graceful_shutdown)
        self.assertEqual(command[2], [ "admin_only" ])

    def test_graceful_shutdown_sends_the_chat_a_goodnight_message(self):
        mock_connection = Connection()
        _message = "irrelevant in this instance"

        stop.graceful_shutdown(mock_connection, _message)

        self.assertEqual(mock_connection._message, Chat.good_night)

    def test_graceful_shutdown_sets_connection_to_stop_running(self):
        mock_connection = Connection()
        _message = "irrelevant in this instance"

        self.assertTrue(mock_connection.keep_IRC_running)
        stop.graceful_shutdown(mock_connection, _message)

        self.assertFalse(mock_connection.keep_IRC_running)
