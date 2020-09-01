import datetime
import logging

class User(object):
    def __init__(self,username):
        self.points = 0
        self.username = username
        self.last_msg_time = datetime.datetime.now()
    def validate_message_time(self):
        if self.last_msg_time + datetime.timedelta(seconds=1) < datetime.datetime.now():
            self.last_msg_time = datetime.datetime.now()
            logging.debug("Validate message time and reset")
            return True
        else:
            return False