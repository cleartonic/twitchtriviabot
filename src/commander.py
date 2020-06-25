import time
import threading
from src.mr_clean import Mr
from src.messages import Log as report

class Commander:
    def __init__(self, commands, admins, connection, log = print, sleep = time.sleep):
        self.log = log
        self.sleep = sleep
        self.commands = commands
        self.admins = [Mr.lower(admin) for admin in admins]
        self.connection = connection
        self.last_response = ('bot', 'No Messages Recieved')

    def listen_for_commands(self):
        while self.connection.keep_IRC_running:
            self.check_connection_last_message()

    def check_connection_last_message(self):
        self.sleep(self.connection.seconds_per_message)
        if self.last_response != self.connection.last_response:
            self.respond_to_new_last_message()

    def respond_to_new_last_message(self):
        self.last_response = self.connection.last_response
        username = self.last_response[0]
        message = self.last_response[1]

        for command in self.commands:
            if message == command[0]:
                self.process_command(username, command)

    def process_command(self, username, command):
        validations = command[2]
        callback = command[1]

        if "admin_only" in validations:
            self.validate_admin(username, command)
        else:
            self.log(report.good_command(username, command[0]))
            self.run_command(username, command, callback)

    def validate_admin(self, username, command):
        callback = command[1]

        if Mr.lower(username) in self.admins:
            self.log(report.good_admin(username, command[0]))
            self.run_command(username, command, callback)
        else:
            self.log(report.bad_admin(username, command[0]))

    def run_command(self, username, command, callback):
        thread = threading.Thread(target=self.listen_for_commands)
        thread.start()
        message = command[0]
        callback(self.connection, (username, message))
        thread.join()
