import re
import time
from .message_config import Chat

class Connection():
    messages_per_second = (120)
    COMMANDLIST = ["!triviastart","!triviaend","!top3","!hint","!bonus","!score","!next","!stop","!loadconfig","!backuptrivia","!loadtrivia","!creator"]

    def __init__(self, connect_to, socket):
        self.keep_IRC_running = True
        self.seconds_per_message = 1 / Connection.messages_per_second
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
            self.do_something_by_username_with_the(response)

    def do_something_by_username_with_the(self, response):
        username = re.search(r"\w+", response).group(0)
        if username == self.name:
            pass
        else:
            pattern = r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :"
            CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
            message = CHAT_MSG.sub("", response)
            cleanmessage = re.sub(r"\s+", "", message, flags=re.UNICODE)
            response_body = ':'.join(response.split(':')[2:])
            print("USER RESPONSE: " + username + " : " + response_body)
            if cleanmessage in connection.COMMANDLIST:
                 print("Command recognized.")
                 trivia_commandswitch(cleanmessage,username)
                 time.sleep(1)
            # try:
            #     if bool(re.match("\\b"+var.qs.iloc[var.session_questionno,2]+"\\b",message,re.IGNORECASE)):   # strict new matching
            #         print("Answer recognized.")
            #         trivia_answer(username, cleanmessage)
            #     if bool(re.match("\\b"+var.qs.iloc[var.session_questionno,3]+"\\b",message,re.IGNORECASE)):   # strict new matching
            #         print("Answer recognized.")
            #         trivia_answer(username, cleanmessage)
            # except:
            #     pass

    def sendmessage(self, message):
        irc_id = ":" + self.name + "!" + self.name + "@" + self.name + ".tmi.twitch.tv"
        answer = irc_id + " PRIVMSG " + self.chan + " : " + message + "\r\n"
        encoded_answer = answer.encode("utf-8")
        self.socket.send(encoded_answer)
