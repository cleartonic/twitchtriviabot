from src.mr_clean import Mr
from .messages import Log as report
from src.messages import Chat

from src.game.triviaset import Trivia_Set
from mocks.game.game_record import Game_Record
from mocks.game.players import Players
from src.game.questioner import Questioner
from src.game.round import Round
from src.game.game import Game

class Commander:
    commands = {
        "start_the_next_trivia_round": "!go",
        "stop_the_bot": "!stop"
    }

    def __init__(self, admins, connection, log):
        self.log = log
        self.admins = [Mr.lower(admin) for admin in admins]
        self.connection = connection
        self.last_response = ('bot', 'No Messages Recieved')

    def listen_for_commands(self):
        while self.connection.keep_IRC_running:
            time.sleep(self.connection.seconds_per_message)
            if self.last_response != self.connection.last_response:
                self.last_response = self.connection.last_response
                username = Mr.lower(self.last_response[0])
                message = Mr.clean(self.last_response[1])

                if message == commands['start_the_next_trivia_round']:
                    self.go(username)
                if message == commands['stop_the_bot']:
                    self.stop(username)

    def go(self, username):
        command = commands['start_the_next_trivia_round']
        if username in self.admins:
            self.spin_up_a_trivia_round(username, command)
        else:
            self.log(report.bad_admin(username, command))

    def stop(self, username):
        command = commands['stop_the_bot']
        if username in self.admins:
            self.graceful_shutdown(username, command)
        else:
            self.log(report.bad_admin(username, command))

    def spin_up_a_trivia_round(self, username, command):
        self.log(report.good_admin(username, command))
        csv = Trivia_Set("mocks/triviaset.csv") # 'triviaset.csv'
        if not csv.error:
            questions = csv.get_questions()
            game = Game(questions, self.connection, Game_Record(), Players())
            game.go()

    def graceful_shutdown(self, username, command):
        self.log(report.good_admin(username, command))
        self.connection.send(Chat.good_night)
        self.connection.keep_IRC_running = False
