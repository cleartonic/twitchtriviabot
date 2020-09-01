import logging
import socket
import time

# INFO_MESSAGE = 'Twitch Trivia Bot loaded. Version %s. Developed by cleartonic. %s' % (VERSION_NUM, random.randint(0,10000))
INFO_MESSAGE = 'Twitch Trivia Bot loaded.'

class ChatBot(object):
    '''
    ChatBot is solely responsible for sending and reporting messages
    '''
    def __init__(self, auth_config):
        self.infomessage = INFO_MESSAGE
        try:
            self.valid = True
            self.bot_config = auth_config
            try:
                self.s = socket.socket()
                self.s.connect((self.bot_config['host'], self.bot_config['port']))
                self.s.send("PASS {}\r\n".format(self.bot_config['pass']).encode("utf-8"))
                self.s.send("NICK {}\r\n".format(self.bot_config['nick']).encode("utf-8"))
                self.s.send("JOIN #{}\r\n".format(self.bot_config['chan']).encode("utf-8"))
                time.sleep(1)
                self.send_message(self.infomessage)
                self.s.setblocking(0)
            except:
                self.s = socket.socket()
                self.s.connect((self.bot_config['host'], self.bot_config['port']))
                self.s.send("PASS {}\r\n".format(self.bot_config['pass']).encode("utf-8"))
                self.s.send("NICK {}\r\n".format(self.bot_config['nick']).encode("utf-8"))
                self.s.send("JOIN #{}\r\n".format(self.bot_config['chan'].lower()).encode("utf-8"))
                time.sleep(1)
                self.send_message(self.infomessage)
                self.s.setblocking(0)       
        except Exception as e:
            logging.debug("Connection failed. Check config settings and reload bot.\nError code:\n%s" % str(e))
            self.valid = False
        logging.debug("Finished setting up Chat Bot.")
        
    ### Chat message sender func
    def send_message(self, msg):
        answermsg = ":"+self.bot_config['nick']+"!"+self.bot_config['nick']+"@"+self.bot_config['nick']+".tmi.twitch.tv PRIVMSG #"+self.bot_config['chan']+" : "+msg+"\r\n"
        encoding = "utf-8"
        try:
            configured_encoding = self.bot_config['encoding'].lower()
            if 'iso' in configured_encoding:
                encoding = configured_encoding
        except:
            pass

        self.s.send(answermsg.encode(encoding))
        
    def retrieve_messages(self):
        username, message, cleanmessage = None, None, None
        try:
            response = self.s.recv(1024).decode("utf-8")
#            logging.debug("Response:\n%s" % response)
            if response == "PING :tmi.twitch.tv\r\n":
                self.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                logging.debug("Pong sent")
            else:
                username = re.search(r"\w+", response).group(0) 
                if username == self.bot_config['nick']:  # Ignore this bot's messages
                    pass
                else:
                    message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :").sub("", response)
                    cleanmessage = re.sub(r"\s +", "", message, flags=re.UNICODE).replace("\n","").replace("\r","")
                    
#                    logging.debug("USER RESPONSE: " + username + " : " + message)
#                    if cleanmessage in var.COMMANDLIST:
#                        logging.debug("Command recognized.")
#                        trivia_commandswitch(cleanmessage,username)
#                        time.sleep(1)
        except: 
#            logging.debug(traceback.print_exc())
            
            pass
        return username, message, cleanmessage