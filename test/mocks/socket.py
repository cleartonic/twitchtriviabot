import random

class socket:
    def socket():
        return socket()

    def connect(self, host_port_tuple):
        print(f'Fake socket connected: {host_port_tuple}')

    def send(self, string):
        print(f'Fake socket was sent: {string}')

    def setblocking(self, int):
        print(f'Fake socket set blocking: {int}')

    def recv(self, int):
        print(f'Fake socket tried to recieve a message in: {int}')
        return fake_reception();

    def decode(self, byte_array):
        print(f'Fake socket tried to decode: {byte_array}')
        return "This is your Fake Server Speaking: Be excellent to each other."

class fake_reception:
        def decode(fake_reception, encoding):
            print(f'Fake reception tried to decode itself: {encoding}')

            fake_server_message = ':FakeServer!FakeServer@FakeServer.tmi.twitch.tv PRIVMSG :This is your Fake Server Speaking: Be excellent to each other.\r\n'
            special_ping_message = 'PING :tmi.twitch.tv\r\n'
            message = random.choice([fake_server_message, special_ping_message])
            return message
