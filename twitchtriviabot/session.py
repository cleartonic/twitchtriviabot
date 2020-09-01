import csv
import datetime
import logging
import itertools
import os
import random
import time
import traceback

from collections import Counter 
from .question import Question
from .user import User

class NullSession():
    trivia_active = False     
    trivia_status = "Inactive"

class Session(object):
    def __init__(self, cb, trivia_config):
        logging.debug("Beging setting up Session...")
        logging.debug("Setting up session constants...")
        self.cb = cb
        self.userscores = {}                         # Dictionary holding user scores, kept in '!' and loaded/created upon trivia. [1,2,3] 1: Session score 2: Total trivia points 3: Total wins
        self.SWITCH = True                           # Switch to keep bot connection running
        self.trivia_active = False                   # Switch for when trivia is being played
        self.questionasked = False            # Switch for when a question is actively being asked
        self.questionasked_time = 0           # Time when the last question was asked (used for relative time length for hints/skip)
        self.questionno = 1                  # Question # in current session
        self.answervalue = 1                 # How much each question is worth (altered by BONUS only)
        self.question_count = 0
        self.questions = []
        self.answered_questions = []
        self.active_question = None
        self.trivia_status = "Inactive"
        self.users = []
        self.admin_commands_list = {'!triviaend':self.force_end_of_trivia,
                                    '!skip':self.skip_question,
                                    '!start':self.start_question,
                                    '!endquestion':self.end_question,
                                    '!next':self.skip_question,
                                    '!bonus':self.toggle_bonus_mode}
        self.commands_list       = {'!score':self.check_user_score}
        self.session_actions = {'hint1':self.call_hint1,
                                'hint2':self.call_hint2,
                                'skip':self.skip_question}

        self.TIMER = 0                               # Ongoing active timer 
        self.bonus_round = False              
        
        
        logging.debug("Loading config...")
        self.session_config = trivia_config
        self.admins = [i.strip() for i in trivia_config['admins'].split(",")]
        out_str = ''
        for k, v in self.session_config.items():
            out_str += "   " + "{:<20}".format(k)+ " " + str(v) + "\n"
        logging.debug(out_str)
        self.valid = True
        try:
            if self.session_config['music_mode']:
                # in music mode, do not load a trivia set, instead do nothing
                self.question_count = 99999
                self.ts = {}
                self.ss = {}
                
            else:
                logging.debug("Loading trivia data...")
                
                with open(os.path.join('config',self.session_config['file_name']),'r') as f:
                    data = f.read()            
                data = csv.reader(data.splitlines(),quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
                self.ts = {}
                for idx, i in enumerate(data):
                    category, question, answer, answer2, creator = i
                    self.ts[idx] = {'category':category, 'question':question, 'answer':answer,'answer2':answer2,'creator':creator}
    
                if self.session_config['mode'] == 'poll2':
                    logging.debug("Mode set to poll2, only taking questions with valid answer/answer2...")
                    valid_keys = [i for i in self.ts if self.ts[i]['answer2'] != '']
                    new_ts = {}
                    for i in valid_keys:
                        new_ts[i] = self.ts[i]
                    self.ts = new_ts
                
                self.tsrows = len(self.ts.keys())
    
                if self.tsrows < self.session_config['question_count']:
                    self.session_config['question_count'] = int(self.tsrows)
                    logging.debug("Warning: Trivia questions for session exceeds trivia set's population. Setting session equal to max questions.")
    
    
                logging.debug("Creating session set data. Population %s, session %s" % (self.tsrows, self.session_config['question_count']))
                chosen_idx = random.sample(list(self.ts.keys()), int(self.session_config['question_count']))
                if self.session_config['order'] == 'ordered':
                    chosen_idx.sort()
                self.ss = {}
                for i in chosen_idx:
                    self.ss[i] = self.ts[i]
                try:
    
                    for k, v in self.ss.items():
                        self.questions.append(Question(v, self.session_config))
                except Exception as e:
                    logging.debug("Error %s on question creation" % e)
                if self.session_config['length'] == 'infinite':
                    self.question_count = 99999
                else:
                    self.question_count = len(self.questions)
    
                logging.debug("Finished setting up Session.")
        except Exception as e:
            logging.debug("Error on data load. Check trivia set and make sure file_name matches in config, and that file matches columns/headers correctly\nError code:\n>> %s" % e)
            self.valid = False
                
    

        if str(self.session_config['output']).lower() == 'true' or self.session_config['output'] == True:
            for i in ['1_place_username','1_place_score','2_place_username','2_place_score','3_place_username','3_place_score','scoreboard']:
                with open(self.get_config_path('scores','%s.txt' % i),'w') as f:
                    f.write('')

    def get_config_path(self, *args):
        return os.path.join(*itertools.chain((self.session_config['path_dir'],), args))

    def call_current_time(self):
        return datetime.datetime.now()
    def report_question_numbers(self):
        if self.session_config['length'] == 'infinite':
            return "%s / %s" % (self.questionno, "inf")
        else:
            return "%s / %s" % (self.questionno, self.question_count)
    def call_question(self):
        if self.session_config['music_mode']:
            try:
                # create the question based on config/music/ contents each time
                with open(self.get_config_path('music','artist.txt'),'r') as f:
                    artist = f.read()
                with open(self.get_config_path('music','track.txt'),'r') as f:
                    track = f.read()
                self.active_question = Question([artist,track],self.session_config,music_mode=True)
                self.active_question.activate_question(self.bonus_round, int(self.session_config['question_bonusvalue']))
                self.questionasked = True
                self.cb.send_message("Question %s: %s" % (self.questionno, self.active_question.question_string))
                logging.debug(self.active_question)
            except Exception as e:
                logging.debug("Error on calling next question, ending trivia...%s" % str(e))
                self.force_end_of_trivia()
            
        else:        
            try:
                self.active_question = self.questions.pop()
                if self.session_config['length'] == 'infinite':
                    # add the question back, to the start of the index (so its not popped next)
                    self.questions = [self.active_question] + self.questions
                self.active_question.activate_question(self.bonus_round, int(self.session_config['question_bonusvalue']))
                self.questionasked = True
                self.cb.send_message("Question %s: %s" % (self.questionno, self.active_question.question_string))
                logging.debug(self.active_question)
            except:
                logging.debug("Error on calling next question, ending trivia...")
                self.force_end_of_trivia()
        self.write_question_variable()


    def question_answered(self, user, answer_slot=None):
        if self.session_config['mode'] == 'single':
            user.points += self.active_question.point_value
            self.active_question.active = False
            self.answered_questions.append(self.active_question)
            self.cb.send_message(self.active_question.answer_string(user, self.questionno))
            self.questionno += 1
            self.questionasked = False
            time.sleep(self.session_config['question_delay'])
            if self.questionno < self.question_count + 1:
                try:
                    self.call_question()
                except:
                    logging.debug("Error on question call %s" % traceback.print_exc() )
            else:
                self.force_end_of_trivia()

            
        elif self.session_config['mode'] == 'poll':
            if user not in self.active_question.answered_user_list:
                self.active_question.answered_user_list.append(user)
        elif self.session_config['mode'] == 'poll2':
            if answer_slot == 1:
                if user not in self.active_question.answered_user_list:
                    self.active_question.answered_user_list.append(user)
            elif answer_slot == 2:
                if user not in self.active_question.answered_user_list2:
                    self.active_question.answered_user_list2.append(user)
        if str(self.session_config['output']).lower() == 'true' or self.session_config['output'] == True:
            self.output_session_variables()
            
        self.clear_question_variable()
            
    def write_question_variable(self):
        try:
            with open(self.get_config_path('scores','question.txt'),'w') as f:
                f.write(self.active_question.question_string)        
        except:
            logging.error("Error on write question to file")

    def clear_question_variable(self):
        try:
            with open(self.get_config_path('scores','question.txt'),'w') as f:
                f.write("")      
        except:
            logging.error("Error on write question to file")
            
    def output_session_variables(self):
        try:
            user_dict = {}
            for u in self.users:
                user_dict[u.username] = u.points
            if user_dict:
                k = Counter(user_dict)
                top3 = k.most_common(3)
                for idx, i in enumerate(top3):
                    with open(self.get_config_path('scores','%s_place_username.txt' % (int(idx) + 1)),'w') as f:
                        f.write(str(i[0]))
                    with open(self.get_config_path('scores','%s_place_score.txt' % (int(idx) + 1)),'w') as f:
                        f.write(str(i[1]))
            
                return_str = ''
                for k, v in user_dict.items():
                    return_str += '%s: %s\n' % (k,v)
                with open(self.get_config_path('scores','scoreboard.txt'),'w') as f:
                    f.write(return_str)


        except:
            logging.debug("Error on output session variables method (score txt files) %s" % traceback.print_exc())


        
    def check_user(self,username):
        '''
        This checks the username and returns the User object that matches
        '''
        for user in self.users:
            if user.username == username:
                logging.debug("Returning found user %s" % username)
                return user
        else:
            logging.debug("Creating new user %s" % username)
            new_user = User(username)
            self.users.append(new_user)
            return new_user
    def check_user_score(self, user, from_trivia_bot = False):
        if not from_trivia_bot:
            if user.validate_message_time():
                self.cb.send_message("User %s has %s points." % (user.username, user.points))
        else:
            self.cb.send_message("User %s had %s points last game." % (user.username, user.points))
        
    def check_top_3(self):
        user_dict = {}
        for u in self.users:
            user_dict[u.username] = u.points
        if user_dict:
            k = Counter(user_dict)
            top3 = k.most_common(3)
            return_str = ''
            for i in top3:
                return_str += '%s: %s\n' % (i[0], i[1])
            return return_str
        else:
            return "No users"
        

        
    def force_end_of_trivia(self):
        self.check_end_of_trivia(end_trivia_flag=True)
    def check_end_of_trivia(self, end_trivia_flag = False):
        if (self.questionno > self.question_count and self.trivia_active) or end_trivia_flag:
            self.write_question_variable()
            logging.debug("Ending trivia...")
            self.trivia_active = False
            self.find_winner()
            if self.winners:
                try:
                    if len(self.winners) > 1:
                        winners_string = ', '.join([i.username for i in self.winners])
                        self.cb.send_message("Trivia is over - a tie between %s for %s points!" % (winners_string, self.winners[0].points))
                    else:
                        winner = self.winners[0]
                        self.cb.send_message("Trivia is over - %s wins with %s points!" % (winner.username, winner.points))
                except:
                    self.cb.send_message("Error on calculating winners: %s" % (self.winners))
            else:
                self.cb.send_message("Trivia is over - no winner found.")
            time.sleep(.5)
            self.cb.send_message("Thanks for playing!")
            self.trivia_status = "Finished"
            return True
        else:
            return False
        
    def find_winner(self):
        top_score = 0
        for user in self.users:
            if user.points > top_score:
                top_score = user.points
                
        # now check if there's more than 1 winner
        winners = [user for user in self.users if user.points == top_score]
        
        if not winners or top_score == 0:
            winners = None
        
        self.winners = winners

    def call_hint1(self):
        try:
            if self.questionasked:
                self.cb.send_message(self.active_question.hint_1)
        except:
            logging.debug("Error on hint 1 %s" % traceback.print_exc())
    def call_hint2(self):
        try:
            if self.questionasked:
                self.cb.send_message(self.active_question.hint_2)
        except:
            logging.debug("Error on hint 1 %s" % traceback.print_exc())

        
    def skip_question(self):
        try:
            self.cb.send_message("Question being skipped. The answer was ** %s **." % self.active_question.answers[0])
            self.active_question.active = False
            self.answered_questions.append(self.active_question)
            self.questionno += 1
            self.questionasked = False
            time.sleep(self.session_config['question_delay'])
            if self.questionno < self.question_count + 1:
                try:
                    self.call_question()
                except:
                    logging.debug("Error on question call %s" % traceback.print_exc() )
            else:
                self.force_end_of_trivia()

            
        except:
            logging.debug("Error on skip question %s" % traceback.print_exc())
    
    def start_question(self):
        try:
            if not self.active_question.active:
                self.call_question()
            else:
                logging.debug("Question already active, ignoring Start Q command")
        except:
            logging.debug("Error on start question %s" % traceback.print_exc())
        
    def end_question(self):
        try:
            self.active_question.question_time_start = datetime.datetime(1990,1,1)

            
        except:
            logging.debug("Error on skip question %s" % traceback.print_exc())
            
    def manage_poll_question(self):
        adjuster = datetime.timedelta(seconds = self.session_config['skip_time'])
        adj_time = self.active_question.question_time_start + adjuster
        cur_time = self.call_current_time()
        if adj_time < cur_time and self.active_question.active:
            logging.debug("Scoring current question for poll")
            self.active_question.find_poll_score()
            self.active_question.active = False
            self.answered_questions.append(self.active_question)
            if self.active_question.point_dict:
                first_user = list(self.active_question.point_dict.keys())[0]
                for user in self.active_question.point_dict:                
                    user.points += self.active_question.point_dict[user]
                self.answered_questions.append(self.active_question)
                self.cb.send_message(self.active_question.answer_string_poll(first_user, self.active_question.point_dict[first_user], self.questionno))
            else:
                self.cb.send_message("Question not answered in time. The answer was ** %s **." % self.active_question.answers[0])

            if self.active_question.session_config['mode'] == 'poll2':
                
                time.sleep(.25)
                # first score second question
                if self.active_question.point_dict2:
                    try:
                        first_user = list(self.active_question.point_dict2.keys())[0]
                        for user in self.active_question.point_dict2:                
                            user.points += self.active_question.point_dict2[user]
                        time.sleep(.5)
                        self.cb.send_message(self.active_question.answer_string_poll2(first_user, self.active_question.point_dict2[first_user], self.questionno))
                    except:
                        logging.debug("Error on second question poll, ignoring.")
                else:
                    self.cb.send_message("2nd category question not answered in time. The answer was ** %s **." % self.active_question.answers[1])

                # then bonus points for both
                
                bonus_users = []
                for user in self.active_question.point_dict.keys():
                    if user in self.active_question.point_dict2.keys():
                        bonus_users.append(user)
                        user.points += 2
                
                if bonus_users:
                    time.sleep(.25)
                    if len(bonus_users) > 3:
                        self.cb.send_message("More than 3 players answered both prompts correctly, yielding +2 bonus points!")
                    else:
                        self.cb.send_message("%s answered both prompts correctly, yielding +2 bonus points!" % ', '.join([user.username]))
            self.questionno += 1
            self.questionasked = False            
    
            # if music_mode is True, then do nothing after a question is answered 
            if self.session_config['music_mode']:
                pass                
            
            else:
                time.sleep(self.session_config['question_delay'])
                if self.questionno < self.question_count + 1:
                    try:
                        self.call_question()
                    except:
                        logging.debug("Error on question call %s" % traceback.print_exc() )
                else:
                    self.force_end_of_trivia()

    def check_actions(self):
        try:
            # first check the question object by seeing if a hint or timeout needs to occur
            action = self.active_question.check_actions()
            if action:
                if action in self.session_actions.keys():
                    func = self.session_actions[action]
                    func()
        except:
            logging.debug("Error on check_actions: %s" % traceback.print_exc())
    def toggle_bonus_mode(self):
        if self.bonus_round:
            self.bonus_round = False
            self.active_question.point_value = 1
            self.cb.send_message("Bonus round disabled. Trivia questions worth 1 point." )
        else:
            self.bonus_round = True
            self.active_question.point_value = int(self.session_config['question_bonusvalue'])
            self.cb.send_message("Bonus round is active! Bonus questions are worth ** %s ** points!" % (self.session_config['question_bonusvalue']))
    def handle_session_message(self,username, message):
        '''
        This is the main function that decides what to do based on the latest message that came in
        For the SESSION
        '''
        self.check_end_of_trivia()
        if message:
            logging.debug("Session vars trivia_active: %s questionasked: %s" % (self.trivia_active, self.questionasked))
            
            user = self.check_user(username)

            # handle commands first
            if message in self.admin_commands_list.keys() and user.username in self.admins:
                func = self.admin_commands_list[message]
                func()
            if message in self.commands_list:
                func = self.commands_list[message]
                func(user)

            # trivia active
            if self.trivia_active:
                if self.questionasked:                    
                    if self.session_config['mode'] == 'poll2':
                        match, answer_slot = self.active_question.check_match(message)
                        if match:
                            self.question_answered(user, answer_slot)                  
                    else:
                        match = self.active_question.check_match(message)
                        if match:
                            self.question_answered(user)
        else:
            return None
