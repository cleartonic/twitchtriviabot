import unittest
from mocks.connection import Connection
from src.commands import stop

class StopCommandTestCase(unittest.TestCase):
    def test_tuple_returns_the_configured_command_tuple(self):
        command = stop.tuple()
        self.assertEqual(command[0], "!stop")
        self.assertEqual(command[1], stop.graceful_shutdown)
        self.assertEqual(command[2], [ "admin_only" ])
