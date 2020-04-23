import re

class Connection():
    keep_IRC_running = True

    HOST = 'INIT' # Variables for IRC / Twitch chat function
    PORT = 'INIT'
    NICK = 'INIT'
    PASS = 'INIT'
    CHAN = 'INIT'
    RATE = (120) # messages per second
    CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
