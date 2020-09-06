from src.messages import Log as report
from mocks import socket as mock_socket
import socket as real_socket
import getopt
import sys

go_live = "go-live"
dry_run = "dry-run"
no_short_options = ""
long_options = [ go_live, dry_run ]

mock_config = 'mocks/config.txt'
real_config = 'config.txt'

class Option_Worker():
    def objectify():
        pass

    def __init__(self, input, log = print):
        self.input = input
        self.log = log
        self.optionNames = Option_Worker.objectify()

    def setWithOptions(self):
        opt_tuple = self.validateInput()

        config_file = 'not configured yet'
        socket = 'not configured yet'
        option = opt_tuple[0][0][0]

        if option == f"--{go_live}":  
            config_file = real_config
            socket = real_socket.socket()
        elif option == f"--{dry_run}":
            config_file = mock_config
            socket = mock_socket.socket()
        else:
            self.log("Hey Dev, did you forget to add your new option into the ever-increasing conditional block in option_worker.py?")
            self.log("Or maybe you borked the early return that checks that only one option may be used.")
            self.log("Might want to consider refactoring that along with this message...")
            sys.exit()
        
        return (config_file, socket)

    def validateInput(self):
        try:
            optTuple = getopt.getopt(self.input, no_short_options, long_options)
        except getopt.GetoptError:
            self.log(report.options_bad)
            self.log_and_exit()

        if len(optTuple[0]) > 1:
            self.log(report.too_many_options)
            self.log_and_exit()

        if len(optTuple[0]) == 0:
            self.log(report.options_too_few)
            self.log_and_exit()

        return optTuple

    def log_and_exit(self):
        self.log(report.log_options(long_options))       
        sys.exit()