import unittest
from mocks.socket import socket
from mocks.time import Time
from mocks.silent_log import dont_print
from mocks.spy_log import Spy_Log
from src.messages import Chat
from src.messages import Log
from src.connection import Connection as Subject

class ConnectionTestCase(unittest.TestCase):
    def test_connection_successfully_connects_to_twitch(self):
        what_blocking_should_be_set_to = 0
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'crash_test_dummy_bot',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        spy_log = Spy_Log()
        dont_sleep = Time(dont_print).sleep

        Subject(connect_to, socket.socket(spy_log.log), dont_print, dont_sleep)

        self.assertEqual(spy_log._history[0], ('some_twitch_url', 1701))
        self.assertEqual(spy_log._history[1], b'PASS oauth:1337_P@SSw0rd123\r\n')
        self.assertEqual(spy_log._history[2], b'NICK crash_test_dummy_bot\r\n')
        self.assertEqual(spy_log._history[3], b'JOIN #home_shopping_network\r\n')
        self.assertEqual(spy_log._history[-1], what_blocking_should_be_set_to)

    def test_connection_sends_twitch_a_greeting_on_connection(self):
        my_id = b':nick_BOTtom!nick_BOTtom@nick_BOTtom.tmi.twitch.tv '
        address = b'PRIVMSG #home_shopping_network :'
        message = Chat.good_morning.encode('utf-8')
        crlf = b'\r\n'
        expected_message = my_id + address + message + crlf
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        spy_log = Spy_Log()
        dont_sleep = Time(dont_print).sleep

        Subject(connect_to, socket.socket(spy_log.log), dont_print, dont_sleep)

        self.assertEqual(spy_log._history[-2], expected_message)

    def test_connection_sleeps_for_a_second_before_sending_twitch_a_greeting(self):
        my_id = b':nick_BOTtom!nick_BOTtom@nick_BOTtom.tmi.twitch.tv '
        address = b'PRIVMSG #home_shopping_network :'
        message = Chat.good_morning.encode('utf-8')
        crlf = b'\r\n'
        expected_message = my_id + address + message + crlf
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        spy_log = Spy_Log()
        spy_on_sleep = Time(spy_log.log).sleep

        Subject(connect_to, socket.socket(spy_log.log), dont_print, spy_on_sleep)

        self.assertEqual(spy_log._history[-3], 'slept for 1 second(s)')
        self.assertEqual(spy_log._history[-2], expected_message)

    def test_logs_a_series_of_feedback_reports_as_it_connects(self):
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        spy_log = Spy_Log()
        dont_sleep = Time(dont_print).sleep

        Subject(connect_to, socket.socket(dont_print), spy_log.log, dont_sleep)

        self.assertEqual(spy_log._history[0], Log.connect_loading)
        self.assertEqual(spy_log._history[1], Log.connect_pass)
        self.assertEqual(spy_log._history[2], Log.connect_nick)
        self.assertEqual(spy_log._history[3], Log.connect_join)
        self.assertEqual(spy_log._history[4], Log.connect_hi)
        self.assertEqual(spy_log._history[5], Log.connect_complete)
        self.assertEqual(len(spy_log._history), 6)

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
        dont_sleep = Time(dont_print).sleep
        s = Subject(connect_to, socket.socket(spy_log.log), dont_print, dont_sleep)

        s.send(body)

        self.assertEqual(spy_log._history[-1], expected_message)

    def test_connection_returns_poorly_formatted_messages_from_twitch(self):
        first_word = "Badabing"
        whole_bad_message = f"{first_word} BAD FORMAT: U shoes r peanut butter."
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        dont_sleep = Time(dont_print).sleep
        mock_socket = socket.socket(dont_print, whole_bad_message)
        s = Subject(connect_to, mock_socket, dont_print, dont_sleep)

        s.scan()

        self.assertEqual(s.last_response[0], first_word)
        self.assertEqual(s.last_response[1], whole_bad_message)

    def test_connection_recieves_properly_formatted_messages_from_twitch(self):
        user = "happy_lass"
        body = "Your shoes are made of peanut butter. Woot!"
        message = f':{user}!{user}@{user}.tmi.twitch.tv PRIVMSG #t_tv :{body}'
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "t_tv"
        }
        dont_sleep = Time(dont_print).sleep
        mock_socket = socket.socket(dont_print, message)
        s = Subject(connect_to, mock_socket, dont_print, dont_sleep)

        s.scan()

        self.assertEqual(s.last_response, (user, body))

    def test_connection_logs_messages_recieved(self):
        user = "happy_lass"
        body = "Woot!"
        message = f':{user}!{user}@{user}.tmi.twitch.tv PRIVMSG #t_tv :{body}'
        expected_print = Log.connect_response(user, body)
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "t_tv"
        }
        dont_sleep = Time(dont_print).sleep
        spy_log = Spy_Log()
        mock_socket = socket.socket(dont_print, message)
        s = Subject(connect_to, mock_socket, spy_log.log, dont_sleep)

        s.scan()

        self.assertEqual(spy_log._history[-1], expected_print)

    def test_connection_ignores_messages_from_itself_sent_from_twitch(self):
        user = "nick_BOTtom"
        body = "Your shoes are made of peanut butter. Woot!"
        message = f':{user}!{user}@{user}.tmi.twitch.tv PRIVMSG #t_tv :{body}'
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': user,
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "t_tv"
        }
        dont_sleep = Time(dont_print).sleep
        mock_socket = socket.socket(dont_print, message)
        s = Subject(connect_to, mock_socket, dont_print, dont_sleep)

        s.scan()

        self.assertEqual(s.last_response, ('bot', 'No Messages Recieved'))

    def test_connection_doesnt_keep_ignored_messages_sent_from_twitch(self):
        bot = "nick_BOTtom"
        user = "happy_lass"
        body = "Your shoes are made of peanut butter. Woot!"
        last_user_message = (user, body)
        message = f':{user}!{user}@{user}.tmi.twitch.tv PRIVMSG #t_tv :{body}'
        bot_message = f':{bot}!{bot}@{bot}.tmi.twitch.tv PRIVMSG #t_tv :{body}'
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "t_tv"
        }
        dont_sleep = Time(dont_print).sleep
        mock_socket = socket.socket(dont_print, message)
        s = Subject(connect_to, mock_socket, dont_print, dont_sleep)

        s.scan()

        self.assertEqual(mock_socket.message, message)
        self.assertEqual(s.last_response, last_user_message)

        mock_socket.message = bot_message
        s.scan()

        self.assertEqual(mock_socket.message, bot_message)
        self.assertEqual(s.last_response, last_user_message)
        self.assertNotEqual(s.last_response, (bot, body))
        self.assertNotEqual(s.last_response, ('bot', 'No Messages Recieved'))

    def test_connection_doesnt_log_ignored_messages_sent_from_twitch(self):
        user = "happy_lass"
        bot = "nick_BOTtom"
        body = "Woot!"
        message = f':{user}!{user}@{user}.tmi.twitch.tv PRIVMSG #t_tv :{body}'
        bot_message = f':{bot}!{bot}@{bot}.tmi.twitch.tv PRIVMSG #t_tv :{body}'
        expected_print = "Chat Message From: happy_lass : Woot!"
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': bot,
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "t_tv"
        }
        dont_sleep = Time(dont_print).sleep
        spy_log = Spy_Log()
        mock_socket = socket.socket(dont_print, message)
        s = Subject(connect_to, mock_socket, spy_log.log, dont_sleep)

        s.scan()

        self.assertEqual(spy_log._history[-1], expected_print)

        mock_socket.message = bot_message
        s.scan()

        self.assertEqual(spy_log._history[-1], expected_print)
        self.assertTrue(bot not in spy_log._history[-1])

    def test_connection_doesnt_report_pings(self):
        message = 'PING :tmi.twitch.tv\r\n'
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "t_tv"
        }
        dont_sleep = Time(dont_print).sleep
        mock_socket = socket.socket(dont_print, message)
        s = Subject(connect_to, mock_socket, dont_print, dont_sleep)

        s.scan()

        self.assertEqual(s.last_response, ('bot', 'No Messages Recieved'))

    def test_connection_pongs_when_pinged(self):
        ping = 'PING :tmi.twitch.tv\r\n'
        pong = b'PONG :tmi.twitch.tv\r\n'
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "t_tv"
        }
        dont_sleep = Time(dont_print).sleep
        spy_log = Spy_Log()
        mock_socket = socket.socket(spy_log.log, ping)
        s = Subject(connect_to, mock_socket, dont_print, dont_sleep)

        s.scan()

        self.assertEqual(spy_log._history[-1], pong)

    def test_connection_logs_its_pongs(self):
        ping = 'PING :tmi.twitch.tv\r\n'
        pong_log = Log.connect_pong
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "t_tv"
        }
        dont_sleep = Time(dont_print).sleep
        spy_log = Spy_Log()
        mock_socket = socket.socket(dont_print, ping)
        s = Subject(connect_to, mock_socket, spy_log.log, dont_sleep)

        s.scan()

        self.assertEqual(spy_log._history[-1], pong_log)

    def test_connection_doesnt_recieve_messages_too_fast(self):
        connect_to = {
            'irc_url':'some_twitch_url',
            'irc_port': 1701,
            'bot_name': 'nick_BOTtom',
            'oauth_token': 'oauth:1337_P@SSw0rd123',
            'channel': "home_shopping_network"
        }
        spy_log = Spy_Log()
        spy_on_sleep = Time(spy_log.log).sleep
        mock_socket = socket.socket(dont_print)
        s = Subject(connect_to, mock_socket, dont_print, spy_on_sleep)

        scan_rate = s.seconds_per_message
        s.scan()

        self.assertEqual(scan_rate, 1 / 120 )
        self.assertEqual(spy_log._history[-1], f'slept for {scan_rate} second(s)')
