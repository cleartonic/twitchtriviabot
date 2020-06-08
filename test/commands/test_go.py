import unittest
from mocks.connection import Connection
from src.commands import go

class GoCommandTestCase(unittest.TestCase):
    def test_tuple_returns_the_configured_command_tuple(self):
        subject = go()
        command = subject.tuple()
        self.assertEqual(command[0], "!go")
        self.assertEqual(command[1], subject.run_the_next_trivia_round)
        self.assertEqual(command[2], [ "admin_only" ])
