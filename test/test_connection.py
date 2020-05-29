import unittest
from mocks import socket
from mocks.silent_log import dont_print
from mocks.spy_log import Spy_Log
from src.connection import Connection as Subject

class ConnectionTestCase(unittest.TestCase):
    def test_connection_successfully_connects_to_twitch(self):
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'crash_test_dummy_bot',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        spy_log = Spy_Log()
        what_blocking_should_be_set_to = 0
        sleep_time = 0
        Subject(connect_to, socket.socket(spy_log.log), dont_print, sleep_time)
        self.assertEqual(spy_log._history[0], ('some_twitch_url', 1701))
        self.assertEqual(spy_log._history[1], b'PASS oauth:1337_P@SSw0rd123\r\n')
        self.assertEqual(spy_log._history[2], b'NICK crash_test_dummy_bot\r\n')
        self.assertEqual(spy_log._history[3], b'JOIN home_shopping_network\r\n#')
        self.assertEqual(spy_log._history[-1], what_blocking_should_be_set_to)

    def test_connection_sends_twitch_a_greeting_on_connection(self):
        my_id = b':nick_BOTtom!nick_BOTtom@nick_BOTtom.tmi.twitch.tv '
        address = b'PRIVMSG #home_shopping_network :'
        msg_p1 = b'Refactored out of a cleartonic fork by @LtJG_Bodhi_Cooper: '
        msg_p2 = b'Trivvy Bot V-2.0 has been called into existence.\r\n'
        expected_message = my_id + address + msg_p1 + msg_p2
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        spy_log = Spy_Log()
        sleep_time = 0
        Subject(connect_to, socket.socket(spy_log.log), dont_print, sleep_time)
        self.assertEqual(spy_log._history[-2], expected_message)

    def test_connection_sends_twitch_arbitrary_messages(self):
        my_id = b':nick_BOTtom!nick_BOTtom@nick_BOTtom.tmi.twitch.tv '
        address = b'PRIVMSG #home_shopping_network :'
        body = "My cat's breath smells like cat food."
        crlf = b'\r\n'
        expected_message = my_id + address + body.encode('utf-8') + crlf
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        spy_log = Spy_Log()
        sleep_time = 0
        s = Subject(connect_to, socket.socket(spy_log.log), dont_print, sleep_time)
        s.send(body)
        self.assertEqual(spy_log._history[-1], expected_message)
