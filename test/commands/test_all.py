import unittest
import inspect
from src.commands import all

class AllCommandsTestCase(unittest.TestCase):
    def test_commands_returns_tuples_with_message_matchers(self):
        subject = all.commands()

        for command in subject:
            message_matcher = command[0]
            self.assertEqual(type(message_matcher), str)
            self.assertNotEqual(message_matcher, "")

    def test_commands_returns_a_tuple_with_callbacks(self):
        subject = all.commands()

        for command in subject:
            callback = command[1]
            self.assertTrue(callable(callback))
            params = inspect.signature(callback).parameters

            class_signature = 'self'
            if class_signature in params:
                self.assertEqual(len(params), 3)
            else:
                self.assertEqual(len(params), 2)


    def test_commands_returns_a_tuple_with_validations(self):
        subject = all.commands()
        valid_validations = [ "admin_only" ]

        for command in subject:
            validations = command[2]
            self.assertEqual(type(validations), list)
            for validation in validations:
                self.assertTrue(validation in valid_validations)

    def test_commands_does_not_contain_name_collisions(self):
        subject = all.commands()
        command_messages = []
        unique = []
        for command in subject:
            command_messages.append(command[0])
            if command[0] not in unique:
                unique.append(command[0])
        self.assertEqual(unique, command_messages)
