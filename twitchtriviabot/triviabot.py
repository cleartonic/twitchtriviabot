import logging
import os
import pickle
import time
import traceback
import yaml

from .chatbot import ChatBot
from .session import NullSession, Session
# SETTINGS
# TriviaBot object sets up and manages Session objects
        
class TriviaBot(object):
    
    def __init__(self):
        logging.debug("Begin setting up Trivia Bot...")
        self.valid = True
        self.trivia_active = False
        self.error_msg = ""
        self.active_session = NullSession()
        with open(os.path.join('config','trivia_config.yml'),'r') as f:
            temp_config = yaml.safe_load(f)
            self.validate_trivia_config(temp_config, os.path.abspath(f.name))
        with open(os.path.join('config','auth_config.yml'),'r') as f:
            temp_config = yaml.safe_load(f)
            self.validate_auth_config(temp_config)
            
        if self.valid:
            try:
                logging.debug("Setting up Chat Bot...")
                self.cb = ChatBot(self.auth_config)
            except:
                logging.debug("Failure to connect to Twitch chat. Check auth config and retry")
                self.valid = False
            self.admin_commands_list = {'!triviastart':self.start_session,
                                  '!stopbot':self.stop_bot,
                                  '!loadsession':self.load_trivia_session,
                                  '!savesession':self.save_trivia_session}
            
            self.commands_list = {'!score':self.check_active_session_score}
            self.admins = [i.strip() for i in self.trivia_config['admins'].split(",")]
                
            logging.debug("Finished setting up Trivia Bot.")
        else:
            logging.debug("Invalid setup - please check trivia_config.yml file")
            
            
    def validate_trivia_config(self,temp_config,config_path):
        for k, v in temp_config.items():
            if k == 'filename':
                if not v.endswith(".csv"):
                    self.error_msg = "Config error: Filename %s does not end with .csv" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k in ['question_count','hint_time1','hint_time2','skip_time','question_delay','question_bonusvalue']:
                if type(v) != int:
                    self.error_msg = "Config error: Error with %s -> %s not being an integer" % (k,v)
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'mode':
                if v not in ['single','poll','poll2']:
                    self.error_msg = "Config error: Mode must be 'single', 'poll', 'poll2'"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'admins':
                if type(v) != str:
                    self.error_msg = "Config error: Admins must be text only, separated by commas"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'order':
                if v not in ['random','ordered']:
                    self.error_msg = "Config error: Order must be 'ordered' or 'random' only"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'music_mode':
                if type(v) != bool:
                    self.error_msg = "Config error: Music mode must be set to true or false"
                    logging.debug(self.error_msg)
                    self.valid = False                 
                if v == True:
                    if "poll2" not in temp_config['mode']:
                        self.error_msg = "Config error: When using music mode, mode 'poll2' must be chosen"
                        logging.debug(self.error_msg)
                        self.valid = False
                    if "infinite" not in temp_config['length']:
                        self.error_msg = "Config error: When using music mode, length 'infinite' must be chosen"
                        logging.debug(self.error_msg)
                        self.valid = False
                    

        if self.valid:
            logging.debug("Passed trivia_config validation.")
            self.trivia_config = temp_config
            self.trivia_config['path_dir'] = os.path.dirname(config_path)
            
    def validate_auth_config(self,temp_config):
        for k, v in temp_config.items():
            if k == 'host':
                if v != 'irc.twitch.tv':
                    logging.debug("Config issue: Host name %s is not default irc.twitch.tv - change at discretion only" % v)
            elif k == 'port':
                if int(v) != 6667:
                    logging.debug("Config issue: Port %s is not default 6667 - change at discretion only" % v)
            elif k == 'nick':
                if type(k) != str:
                    self.error_msg = "Config error: Bot name %s should be text string only" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'pass':
                if "oauth:" not in v:
                    self.error_msg = "Config error: Invalid password %s. Password should be in format 'oauth:xxx'" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'chan':
                if "#" in v or type(v) != str:
                    self.error_msg = "Config error: Invalid channel name %s. Channel name should be text only with NO number sign" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            
                    

        if self.valid:
            logging.debug("Passed auth_config validation.")
            self.auth_config = temp_config
        
    def start_session(self, start_new_override=True):
        logging.debug("Starting session...")
        if not self.trivia_active:
            if not self.active_session or start_new_override: #if there's already a session, ignore, unless from command
                self.active_session = Session(self.cb, self.trivia_config)    
            self.active_session.trivia_status = "Active"
            logging.debug(self.active_session.trivia_status)
            self.cb.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            
            # setup
            try:
                if self.trivia_config['length'] == 'infinite':
                    self.cb.send_message("Trivia has begun! Infinite question mode. Trivia will start in %s seconds." % (self.active_session.session_config['question_delay']))
                else:
                    self.cb.send_message("Trivia has begun! Question Count: %s. Trivia will start in %s seconds." % (self.active_session.question_count, self.active_session.session_config['question_delay']))
                time.sleep(self.active_session.session_config['question_delay'])
                # get first question, ask, then begin loop
                self.active_session.trivia_active = True
                self.trivia_active = True
                self.active_session.call_question()
        
            except:
                logging.debug("Error on session %s" % traceback.print_exc())
        else:
            logging.debug("Trivia active - ignoring command to begin session.")
            
    def save_trivia_session(self):
        '''
        dump trivia session to pickle file
        '''
        if self.active_session and self.trivia_active:
            if self.active_session.trivia_active:
                save_session = self.active_session
                save_session.cb = None
                with open('latest_session.p', 'wb') as p:
                    pickle.dump(save_session,p)
                self.active_session.cb = self.cb
                logging.debug("Latest trivia session saved.")
        else:
            logging.debug("No trivia session saved.")

    def load_trivia_session(self):
        '''
        load trivia session to pickle file
        '''
        if not self.trivia_active:
            with open('latest_session.p', 'rb') as p:
                load_session = pickle.load(p)
                load_session.cb = self.cb
                self.active_session = load_session
            
            logging.debug("Latest trivia session loaded.")
            self.cb.send_message("Latest trivia session loaded. Beginning trivia...")
            self.start_session(False)
            
        else:
            if self.trivia_active:
                logging.debug("Trivia session active, cannot load during session.")
            else:
                logging.debug("No trivia session loaded.")

        
    def stop_bot(self):
        self.cb.send_message("Ending trivia bot. See you next trivia session!")
        self.valid = False
        try:
            self.active_session.valid = False
            self.active_session.trivia_active = False
        except:
            pass
    def handle_triviabot_message(self,username, message):
        '''
        This is the main function that decides what to do based on the latest message that came in
        For the TRIVIA BOT, primarily used for commands
        '''
        if message:
            #user = self.check_user(username) ########## TO DO

            if message in self.admin_commands_list.keys() and username in self.admins:
                func = self.admin_commands_list[message]
                if message == '!score':
                    func(username)
                else:
                    func()

            if message in self.commands_list.keys():
                func = self.commands_list[message]
                if message == '!score':
                    func(username)
                else:
                    func()
            
    def check_active_session_score(self, username):
        '''
        If there's an active session that has not yet been replaced (meaning, the last active 
        session after a game is over), this will allow users to call their scores
        '''
        if self.active_session != None and not self.active_session.trivia_active:
            user = self.active_session.check_user(username)
            # anti spam measure
            if user.validate_message_time():
                if user:
                    self.active_session.check_user_score(user, from_trivia_bot=True)
                else:
                    self.cb.send_message("%s had no points in the last game." % (username))

        
    def handle_active_session(self):
        username, message, clean_message = self.cb.retrieve_messages()
        
        self.handle_triviabot_message(username, clean_message)
        if message and username !='tmi':
            logging.debug(username)
            logging.debug(self.cb.bot_config['nick'])
            logging.debug("Message received:\n%s " % message)
        self.active_session.check_actions()   
        if self.active_session.session_config['mode'] == 'poll' or self.active_session.session_config['mode'] == 'poll2':
            self.active_session.manage_poll_question()
        self.active_session.handle_session_message(username, clean_message)

    def main_loop(self, command_line_mode = True):
        '''
        The main loop is always running from the start
        While trivia is not active, it will check only handle_triviabot_message for incoming messages
        While trivia is active, it will delegate to the active session
        '''
        
        if command_line_mode:
            iternum = 0
            while self.valid:
                iternum += 1
                if iternum % 300 == 0:
                    try:
                        logging.debug("Iternum %s : trivia_active %s active_session.trivia_active %s" % (iternum, self.trivia_active, self.active_session.trivia_active))
                    except:
                        logging.debug("Iternum %s : %s" % (iternum, self.trivia_active))
                        
                if self.active_session.trivia_active:
                    self.handle_active_session()
                else:
                    username, message, clean_message = self.cb.retrieve_messages()
        
                    if message and username !='tmi':
                        logging.debug(username)
                        logging.debug(self.cb.bot_config['nick'])
                        logging.debug("Message received:\n%s " % message)
                        
        
                    if message:
                        if not self.trivia_active: #when a session is NOT running
                            self.handle_triviabot_message(username, clean_message)
                        
                            
                    if self.trivia_active: # when a session is running
                        # check every iteration if trivia is active or not, to set the trivia bot to be inactive
                        if not self.active_session.trivia_active:
                            logging.debug("Setting trivia to inactive based on active_session...")
                            self.trivia_active = False
                        pass


                        
                
    
                time.sleep(1 / 120)
            logging.debug("Trivia bot no longer valid, ending program.")
        else:
            # when not in command line mode, the window program will handle the looping
            if self.active_session.trivia_active:
                self.handle_active_session()
            else:
                username, message, clean_message = self.cb.retrieve_messages()
    
                if message and username !='tmi':
                    logging.debug(username)
                    logging.debug(self.cb.bot_config['nick'])
                    logging.debug("Message received:\n%s " % message)
                    
    
                if message:
                    if not self.trivia_active: #when a session is NOT running
                        
                        # if theres a command thats recognized, the loop may happen elsewhere
                        # this happens with !triviastart 
                        self.handle_triviabot_message(username, clean_message)
                    
                        
                if self.trivia_active: # when a session is running
                    # check every iteration if trivia is active or not, to set the trivia bot to be inactive
                    if not self.active_session.trivia_active:
                        logging.debug("Setting trivia to inactive based on active_session...")
                        self.trivia_active = False
                    pass