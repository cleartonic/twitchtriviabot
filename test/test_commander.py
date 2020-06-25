import unittest
import time
from concurrent.futures import ThreadPoolExecutor
from mocks.connection import Connection
from mocks.socket import socket
from mocks.time import Time
from mocks.silent_log import dont_print
from mocks.spy_log import Spy_Log
from mocks.command import Spy_Command
from src.messages import Log
from src.commander import Commander as Subject

class CommanderTestCase(unittest.TestCase):
    def test_commander_initializes_with_no_messages_recieved(self):
        commands = []
        admins = []
        s = Subject(commands, admins, Connection(), dont_print)
        self.assertEqual(s.last_response, ('bot', 'No Messages Recieved'))

    def test_commander_case_insensitizes_admin_names(self):
        no_commands = []
        fancy_admins = [
            "dont_change_my_name",
            "PlEaSe_cHaNgE_Me",
            "!#@$_ni!_:="
        ]

        s = Subject(no_commands, fancy_admins, Connection(), dont_print)

        self.assertEqual(s.admins[0], fancy_admins[0])
        self.assertEqual(s.admins[1], "please_change_me")
        self.assertEqual(s.admins[2], fancy_admins[2])

    def test_commander_remembers_the_last_new_message_from_Connection(self):
        no_commands = []
        no_admins = []
        test_response1 = ("gandhi", "Be the change you want to see in the world.")
        test_response2 = ("the_beatles", "Love is all you need.")
        mock_connection = Connection()
        dont_sleep = Time(dont_print).sleep
        s = Subject(no_commands, no_admins, mock_connection, dont_print, dont_sleep)

        mock_connection.last_response = test_response1
        s.check_connection_last_message()

        self.assertEqual(s.last_response, test_response1)

        mock_connection.last_response = test_response2
        s.check_connection_last_message()

        self.assertEqual(s.last_response, test_response2)

    def test_commander_logs_when_a_non_admin_attempts_a_go_command(self):
        command_string = "!go"
        test_response = ("not_an_admin", command_string)
        no_admins = []
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Log()
        commands = [ (command_string, Spy_Command().ping, [ "admin_only" ]) ]
        s = Subject(commands, no_admins, mock_connection, spy.log, dont_sleep)

        mock_connection.last_response = test_response
        s.check_connection_last_message()

        expected_log = Log.bad_admin(test_response[0], test_response[1])
        self.assertEqual(spy._history[-1], expected_log)

    def test_commander_logs_when_a_non_admin_attempts_a_stop_command(self):
        command_string = "!stop"
        test_response = ("not_an_admin", command_string)
        no_admins = []
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Log()
        commands = [ (command_string, Spy_Command().ping, [ "admin_only" ]) ]
        s = Subject(commands, no_admins, mock_connection, spy.log, dont_sleep)

        mock_connection.last_response = test_response
        s.check_connection_last_message()

        expected_log = Log.bad_admin(test_response[0], test_response[1])
        self.assertEqual(spy._history[-1], expected_log)

    def test_commander_does_not_call_command_when_a_non_admin_attempts_an_admin_only_command(self):
        command_string = "!arbitrary_admin_command"
        test_response = ("not_an_admin", command_string)
        no_admins = []
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Command()
        commands = [ (command_string, spy.ping, [ "admin_only" ]) ]
        s = Subject(commands, no_admins, mock_connection, dont_print, dont_sleep)

        mock_connection.last_response = test_response
        s.check_connection_last_message()

        self.assertEqual(len(spy._history), 0)

    def chat(self, connection, response):
        connection.last_response = response
        time.sleep(connection.seconds_per_message)

    def close(self, connection):
        connection.keep_IRC_running = False

    def chat_and_close(self, connection, message):
        self.chat(connection, message)
        self.close(connection)

    def test_commander_calls_command_when_an_admin_attempts_an_admin_only_command(self):
        command_string = "!green_group_stay_close_to_homing_sector_MG-7"
        admins = [ "admiral_akbar" ]
        test_response = (admins[0], command_string)
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Command()
        commands = [ (command_string, spy.ping, [ "admin_only" ]) ]
        s = Subject(commands, admins, mock_connection, dont_print, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_and_close, mock_connection, test_response)

        self.assertEqual(spy._history[-1], test_response)

    def test_commander_ignores_case_of_message_senders(self):
        command_string = "!green_group_stay_close_to_homing_sector_MG-7"
        admins = [ "admIral_akbar" ]
        test_response = ("admiral_Akbar", command_string)
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Command()
        commands = [ (command_string, spy.ping, [ "admin_only" ]) ]
        s = Subject(commands, admins, mock_connection, dont_print, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_and_close, mock_connection, test_response)

        self.assertEqual(spy._history[-1], test_response)

    def test_commander_logs_when_an_admin_makes_an_admin_only_command(self):
        command_string = "!green_group_stay_close_to_homing_sector_MG-7"
        admins = [ "admiral_akbar" ]
        test_response = (admins[0], command_string)
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Log()
        commands = [ (command_string, Spy_Command().ping, [ "admin_only" ]) ]
        s = Subject(commands, admins, mock_connection, spy.log, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_and_close, mock_connection, test_response)

        expected_log = Log.good_admin(admins[0], command_string)
        self.assertEqual(spy._history[-1], expected_log)

    def test_commander_logs_when_any_chat_participant_makes_an_open_command(self):
        command_string = "!everythings_fine_we're_all_fine_here_situation_normal"
        no_admins = []
        test_response = ("han_solo", command_string)
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Log()
        no_validations = []
        commands = [ (command_string, Spy_Command().ping, no_validations) ]
        s = Subject(commands, no_admins, mock_connection, spy.log, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_and_close, mock_connection, test_response)

        expected_log = Log.good_command(test_response[0], command_string)
        self.assertEqual(spy._history[-1], expected_log)

    def test_commander_calls_command_when_a_non_admin_attempts_an_open_command(self):
        command_string = "!arbitrary_open_command"
        test_response = ("not_an_admin", command_string)
        no_admins = []
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Command()
        no_validations = []
        commands = [ (command_string, spy.ping, no_validations) ]
        s = Subject(commands, no_admins, mock_connection, dont_print, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_and_close, mock_connection, test_response)

        self.assertEqual(spy._history[-1], test_response)

    def test_commander_cares_about_exact_command_strings(self):
        command_string = "An Exact String To Match"
        test_response = ("not_an_admin", "!anExact_string-toMATCH")
        no_admins = []
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Command()
        no_validations = []
        commands = [ (command_string, spy.ping, no_validations) ]
        s = Subject(commands, no_admins, mock_connection, dont_print, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_and_close, mock_connection, test_response)

        self.assertEqual(len(spy._history), 0)

    def test_commander_does_not_log_non_existent_commands(self):
        no_commands = []
        admins = ["admiral_akbar"]
        test_response = (admins[0], "!not_a_command")
        expected_log = Log.bad_admin(test_response[0], test_response[1])
        mock_connection = Connection()
        spy = Spy_Log()
        dont_sleep = Time(dont_print).sleep
        s = Subject(no_commands, admins, mock_connection, spy.log, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_and_close, mock_connection, test_response)

        self.assertEqual(len(spy._history), 0)

    def chat_messages(self):
        return [
            ("VILLAGER_1", "Bread!"),
            ("VILLAGER_2", "Apples!"),
            ("VILLAGER_3", "Very small rocks!"),
            ("VILLAGER_1", "Cider!"),
            ("VILLAGER_2", "Uhhh, gravy!"),
            ("VILLAGER_1", "Cherries!"),
            ("VILLAGER_2", "Mud!"),
            ("VILLAGER_3", "Churches -- churches!"),
            ("VILLAGER_2", "Lead -- lead!"),
            ("Arthur", "A duck.")
        ]

    def chat_room(self, connection):
        for message in self.chat_messages():
            self.chat(connection, message)
        self.close(connection)

    def test_commander_can_recieve_commands_from_connection_asynchronously(self):
        test_responses = self.chat_messages()
        command_string = test_responses[3][1]

        no_admins = []
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        spy = Spy_Command()
        no_validations = []
        commands = [ (command_string, spy.ping, no_validations) ]
        s = Subject(commands, no_admins, mock_connection, dont_print, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_room, mock_connection)

        self.assertEqual(spy._history[-1], test_responses[3])
        self.assertEqual(s.last_response, test_responses[-1])

    def test_commander_can_still_recieve_commands_while_a_long_running_process_runs(self):
        test_responses = self.chat_messages()
        expected_penultimate_message = test_responses[0]
        expected_last_command_message = test_responses[-1]
        long_command = expected_penultimate_message[1]
        short_command = expected_last_command_message[1]

        no_admins = []
        dont_sleep = Time(dont_print).sleep
        mock_connection = Connection()
        long_spy = Spy_Command()
        short_spy = Spy_Command()
        no_validations = []
        commands = [
            (long_command, long_spy.long_run, no_validations),
            (short_command, short_spy.ping, no_validations),
        ]
        s = Subject(commands, no_admins, mock_connection, dont_print, dont_sleep)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.listen_for_commands)
            e.submit(self.chat_room, mock_connection)

        self.assertEqual(long_spy._history[-2], expected_penultimate_message)
        self.assertEqual(long_spy._history[-1], (expected_penultimate_message[1], "completed"))
        self.assertEqual(short_spy._history[-1], expected_last_command_message)
        self.assertEqual(len(long_spy._history), 2)
        self.assertEqual(len(short_spy._history), 1)
