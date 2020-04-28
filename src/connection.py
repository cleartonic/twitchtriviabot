import re
import time
import configparser
from .message_config import Chat

class Connection():
    RATE = (120) # messages per second
    # CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    def __init__(self, connect_to, socket):
        self.keep_IRC_running = True
        self.seconds_per_message = 1 / Connection.RATE
        self.host = connect_to['irc_url']
        self.port = connect_to['irc_port']
        self.auth = connect_to['oauth_token']
        self.name = connect_to['bot_name']
        self.chan = connect_to['channel']
        self.socket = socket.socket()
        self.make_initial_twitch_connection()

    def make_initial_twitch_connection(self):
        if self.keep_IRC_running:
            try:
                self.socket.connect((self.host, self.port))
                self.socket.send("PASS {}\r\n".format(self.auth).encode("utf-8"))
                self.socket.send("NICK {}\r\n".format(self.name).encode("utf-8"))
                self.socket.send("JOIN {}\r\n".format(self.chan).encode("utf-8"))
                time.sleep(1)
                self.sendmessage(Chat.infomessage)
                self.socket.setblocking(0)
            except:
                print("Connection failed. Check config settings and reload bot.")
                self.keep_IRC_running = False

    def scan(self):
        try:
            response = self.socket.recv(1024).decode("utf-8")
            self.pong_if_ping(response)
        except:
            pass

    def pong_if_ping(self, response):
        if response == "PING :tmi.twitch.tv\r\n":
            self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong sent")
        else:
            self.do_something_with_the_repsonse_by_username()

    def do_something_with_the_repsonse_by_username(self):
        username = re.search(r"\w+", response).group(0)

    def sendmessage(self, message):
        irc_id = ":" + self.name + "!" + self.name + "@" + self.name + ".tmi.twitch.tv"
        answer = irc_id + " PRIVMSG " + self.chan + " : " + message + "\r\n"
        encoded_answer = answer.encode("utf-8")
        self.socket.send(encoded_answer)
