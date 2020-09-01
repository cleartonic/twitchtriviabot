import datetime
import logging
import re
import traceback

class Question(object):
    '''
    Takes a row from the session set dataframe and converts into object
    '''
    def __init__(self, row, session_config,music_mode=False):
        self.session_config = session_config
        self.active = False
        if music_mode:
            self.question = "Listen to audio..."
            self.answers = [row[0],row[1]]
            self.answers = [i for i in self.answers if i != '']            
            self.category = "Music"
            self.creator = ''
        else:
            self.question = str(row['question'][0]).upper() + row['question'][1:]
            self.answers = [row['answer'],row['answer2']]
            self.answers = [i for i in self.answers if i != '']
            self.category = row['category']
            if 'category' in row:
                self.creator = row['creator']

        if self.session_config['mode'] == 'poll2':
            try:
                answers_temp = [self.answers[0], self.answers[1]]
            except:
                logging.debug("ERROR ON PARSING QUESTION WITH ANSWER/ANSWER2, CHECK TRIVIA SOURCE")

        self.question_string = "%s: %s" % (self.category, self.question)
        self.point_value = 1
        self.set_hints()
        self.hint1_asked = False
        self.hint2_asked = False
        self.skipped = False
        self.answered_user_list =[] # this is an ordered list used for polling multiple answers as they come in
        self.answered_user_list2 =[] # same, but for 2nd during 'poll2' mode
        
    def activate_question(self, bonus_flag, bonus_amount):
        self.active = True
        self.question_time_start = datetime.datetime.now() # datetime object
        if bonus_flag:
            self.point_value = bonus_amount
    
    def __str__(self):
        return "{:<10}".format("Category:") + str(self.category) + "\n" +\
                "{:<10}".format("Question:") + str(self.question) + "\n" +\
                "{:<10}".format("Answers:") + str(self.answers)
                
    def check_match(self, cleanmessage, mode=None):
        if self.session_config['mode'] != 'poll2':
            try:                
                for answer in self.answers:
                    if bool(re.match("\\b%s\\b" % answer,cleanmessage,re.IGNORECASE)):   # strict new matching
                        logging.debug("Answer recognized: %s" % answer)
                        return True
                return False
            except:
                logging.debug("No match on %s to %s" % (cleanmessage, answer))
                return False
            
        else:
            # for poll2, we check each answer for a match and return 
            try:                
                if bool(re.match("\\b%s\\b" % self.answers[0],cleanmessage,re.IGNORECASE)):   # strict new matching
                    logging.debug("Answer recognized: %s" % self.answers[0])
                    return True, 1 # answer_slot 1
                elif bool(re.match("\\b%s\\b" % self.answers[1],cleanmessage,re.IGNORECASE)):   # strict new matching
                    logging.debug("Answer recognized: %s" % self.answers[0])
                    return True, 2 # answer_slot 1
                return False, None
            except:
                logging.debug("Try/except error, no match on %s to %s" % (cleanmessage, answer))
                return False, None
            
    def answer_string(self,user, trivia_num):
        return "%s answers question #%s correctly! The answer is ** %s ** with a %s point value. %s has %s points!" % (user.username, trivia_num ,self.answers[0], self.point_value, user.username, user.points)

    def answer_string_poll(self,user, point_val, trivia_num):
        if self.answered_user_list_remaining:
            return "%s answers question #%s first correctly! The answer is ** %s ** with a %s point value. %s has %s points! Others who answered: %s" % (user.username, trivia_num ,self.answers[0], point_val, user.username, user.points, ', '.join(self.answered_user_list_remaining))
        else:
            return "%s answers question #%s first correctly! The answer is ** %s ** with a %s point value. %s has %s points!" % (user.username, trivia_num ,self.answers[0], point_val, user.username, user.points)

    def answer_string_poll2(self,user, point_val, trivia_num):
        if self.answered_user_list_remaining:
            return "%s answers question (2nd category) #%s first correctly! The answer is ** %s ** with a %s point value. %s has %s points! Others who answered: %s" % (user.username, trivia_num ,self.answers[1], point_val, user.username, user.points, ', '.join(self.answered_user_list_remaining))
        else:
            return "%s answers question (2nd category) #%s first correctly! The answer is ** %s ** with a %s point value. %s has %s points!" % (user.username, trivia_num ,self.answers[1], point_val, user.username, user.points)

    def set_hints(self):
    # type 0, replace 2 out of 3 chars with _
        prehint = str(self.answers[0])
        listo = []
        hint = ''
        counter = 0
        for i in prehint:
            if counter % 3 >= 0.7 and i != " ":
                listo += "_"
            else:
                listo += i
            counter += 1
        for i in range(len(listo)):
            hint += hint.join(listo[i])
        self.hint_1 = hint

        hint2 = re.sub('[aeiou]','_',prehint,flags=re.I)
        self.hint_2 = hint2
    def check_actions(self):
        time_since_question_asked = (datetime.datetime.now() - self.question_time_start).seconds
        
        if (time_since_question_asked >= self.session_config['hint_time1']) and not self.hint1_asked:
            self.hint1_asked = True
            return 'hint1'
        
        elif (time_since_question_asked >= self.session_config['hint_time2']) and not self.hint2_asked:
            self.hint2_asked = True
            return 'hint2'
        
        elif (time_since_question_asked >= self.session_config['skip_time']) and not self.skipped and self.session_config['mode'] == 'single':
            # do not skip on mode 'poll', other process handles
            self.skipped = True
            return 'skip'
                
        else:
            return None
    def find_poll_score(self):
        '''
        for 'poll'/'poll2' mode, this takes the answered_user_list and translates into points
        
        first gets n + 2 points
        second gets n + 1 points
        all others get n points
        where
        n = original point value
        '''
        self.point_dict = {}
        self.answered_user_list_remaining = []
        try:
            if self.answered_user_list:
                self.answered_user_list = self.answered_user_list[::-1]
                self.point_dict = {self.answered_user_list.pop():self.point_value + 2}
                self.answered_user_list_remaining = [i.username for i in self.answered_user_list]
                try:
                    self.point_dict[self.answered_user_list.pop()] = self.point_value + 1
                except:
                    pass
                try:
                    for k in self.answered_list:
                        self.point_dict[k] = self.point_value
                except:
                    pass
            else:
                pass
        except:
            logging.debug("Error on find_poll_score: %s" % traceback.print_exc())
            
            
        # do additional scoring if mode is poll2
        if self.session_config['mode'] == 'poll2':
            self.point_dict2 = {}
            self.answered_user_list_remaining2 = []
            try:
                if self.answered_user_list2:
                    self.answered_user_list2 = self.answered_user_list2[::-1]
                    self.point_dict2 = {self.answered_user_list2.pop():self.point_value + 2}
                    self.answered_user_list_remaining2 = [i.username for i in self.answered_user_list2]
                    try:
                        self.point_dict2[self.answered_user_list2.pop()] = self.point_value + 1
                    except:
                        pass
                    try:
                        for k in self.answered_list2:
                            self.point_dict2[k] = self.point_value
                    except:
                        pass
                else:
                    pass
            except:
                logging.debug("Error on find_poll_score: %s" % traceback.print_exc())
