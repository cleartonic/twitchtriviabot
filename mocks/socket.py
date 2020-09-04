from src.startup.configuration import Configuration
from mocks.silent_log import dont_print
import random

class socket:

    def socket(log = print, message = ""):
        return socket(log, message)

    def __init__(self, log, message):
        self.log = log
        self.message = message

    def connect(self, host_port_tuple):
        self.log(host_port_tuple)

    def send(self, string):
        self.log(string)

    def setblocking(self, int):
        self.log(int)

    def recv(self, int):
        if self.message == '':
            return fake_reception();
        return self.message.encode('utf-8')

class fake_reception:

        def decode(fake_reception, encoding):
            log = dont_print
            config = Configuration('mocks/config.txt', log)
            conn = config.get_connection_constants()
            chan = conn['channel'][1:]
            bot = conn['bot_name']
            admin = random.choice(config.get_admins())

            channel_message = f':{chan}!{chan}@{chan}.tmi.twitch.tv PRIVMSG #{chan} :This is the Trivvy Channel Speaking: Be excellent to each other.\r\n'
            user_message = f':happy_lass!happy_lass@happy_lass.tmi.twitch.tv PRIVMSG #{chan} :Woot!'
            user_answer = f':trivvy_lad!trivvy_lad@trivvy_lad.tmi.twitch.tv PRIVMSG #{chan} :The Great Answer 42'
            user_command = f':trivvy_fan!trivvy_fan@trivvy_fan.tmi.twitch.tv PRIVMSG #{chan} :!score'
            admin_command = f':{admin}!{admin}@{admin}.tmi.twitch.tv PRIVMSG #{chan} :!loadconfig'
            self_message = f':{bot}!{bot}@{bot}.tmi.twitch.tv PRIVMSG #{chan} :You shouldn\'t be seeing this message'
            ping_message = 'PING :tmi.twitch.tv\r\n'
            empty_message = ''

            messages = [channel_message, user_message, user_answer, user_command, admin_command, self_message, ping_message, empty_message]

            return random.choice(messages)
