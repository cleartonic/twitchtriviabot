import re
import time
import configparser
from .message_config import Chat

class Connection():
    RATE = (120) # messages per second
    # CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    def __init__(self, socket):
        self.keep_IRC_running = True
        self.seconds_per_message = 1 / Connection.RATE
        self.socket = socket.socket()
        self.loadconfig()
        self.make_initial_twitch_connection()

    def loadconfig(self):
        print("Bot loaded. Loading config and scores...")
        try:
            self.load_connection_constants()
            print("Config loaded.")
        except:
            print("Config not loaded! Check config file and reboot bot")
            self.keep_IRC_running = False

    def load_connection_constants(self):
        config = configparser.ConfigParser()
        config.read('config.txt')
        self.HOST = str(config['Bot Settings']['HOST'])
        self.PORT = int(config['Bot Settings']['PORT'])
        self.NICK = config['Bot Settings']['NICK']
        self.PASS = config['Bot Settings']['PASS']
        self.CHAN = config['Bot Settings']['CHAN']

    def make_initial_twitch_connection(self):
        if self.keep_IRC_running:
            try:
                self.socket.connect((self.HOST, self.PORT))
                self.socket.send("PASS {}\r\n".format(self.PASS).encode("utf-8"))
                self.socket.send("NICK {}\r\n".format(self.NICK).encode("utf-8"))
                self.socket.send("JOIN {}\r\n".format(self.CHAN).encode("utf-8"))
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
            username = re.search(r"\w+", response).group(0)

    def sendmessage(self, message):
        answermsg = ":"+self.NICK+"!"+self.NICK+"@"+self.NICK+".tmi.twitch.tv PRIVMSG "+self.CHAN+" : "+message+"\r\n"
        answermsg2 = answermsg.encode("utf-8")
        self.socket.send(answermsg2)
