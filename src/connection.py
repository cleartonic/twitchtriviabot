import re
import time
from .messages import Chat
from .messages import Log as report

class Connection():
    ignore_repsonse = ('', '')
    irc_header_pattern = r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :"

    def __init__(self, connect_to, socket, log):
        self.log = log
        self.keep_IRC_running = True
        self.seconds_per_message = 1 / 120
        self.host = connect_to['irc_url']
        self.port = connect_to['irc_port']
        self.auth = connect_to['oauth_token']
        self.name = connect_to['bot_name']
        self.chan = connect_to['channel']
        self.socket = socket.socket()
        self.irc_header = re.compile(Connection.irc_header_pattern)
        self.make_initial_twitch_connection()

    def send(self, message):
        irc_id = f':{self.name}!{self.name}@{self.name}.tmi.twitch.tv'
        answer = f'{irc_id} PRIVMSG #{self.chan} :{message}\r\n'
        encoded_answer = answer.encode("utf-8")
        self.socket.send(encoded_answer)

    def scan(self):
        try:
            response = self.socket.recv(1024).decode("utf-8")
            return self.report(response)
        except:
            return Connection.ignore_repsonse

    def report(self, response):
        if Connection.its_a_ping(response):
            return self.send_a_pong()
        username = re.search(r"\w+", response).group(0)
        if username == self.name:
            return Connection.ignore_repsonse
        response_body = self.irc_header.sub("", response)
        return self.log_and_clean_response(username, response_body)

    def log_and_clean_response(self, username, response_body):
        self.log(report.connect_response(username, response_body))
        clean_response_body = re.sub(r"\s+", "", response_body, flags=re.UNICODE)
        return (username, clean_response_body)

    def its_a_ping(response):
        return response == "PING :tmi.twitch.tv\r\n"

    def send_a_pong(self):
        self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        self.log(report.connect_pong)
        return Connection.ignore_repsonse

    def make_initial_twitch_connection(self):
        if self.keep_IRC_running:
            try:
                self.connect()
                self.send_creds()
                self.send_botname()
                self.join_channel()
                time.sleep(1)
                self.send_hello()
                self.socket.setblocking(0)
                self.log(report.connect_complete)
            except:
                self.log(report.connect_failure)
                self.keep_IRC_running = False

    def connect(self):
        self.log(report.connect_loading)
        self.socket.connect((self.host, self.port))

    def send_creds(self):
        self.log(report.connect_pass)
        self.socket.send("PASS {}\r\n".format(self.auth).encode("utf-8"))

    def send_botname(self):
        self.log(report.connect_nick)
        self.socket.send("NICK {}\r\n".format(self.name).encode("utf-8"))

    def join_channel(self):
        self.log(report.connect_join)
        self.socket.send("JOIN {}\r\n#".format(self.chan).encode("utf-8"))

    def send_hello(self):
        self.log(report.connect_hi)
        self.send(Chat.good_morning)
