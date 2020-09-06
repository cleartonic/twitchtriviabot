from src.game.triviaset import Trivia_Set
from src.game.game import Game
from src.messages import Log as report

class Go:
    command = "!go"
    validate = [ "admin_only" ]

    def __init__(self, question_csv, game_record, players, log = print):
        self.csv_filename = question_csv
        self.record = game_record
        self.players = players
        self.log = log
        self.game_running = False

    def tuple(self):
        return (Go.command, self.run_the_next_trivia_round, Go.validate)

    def run_the_next_trivia_round(self, connection, message):
        if self.game_running:
            self.log(report.in_progress(message[0], message[1]))
        else:
            self.lock_run_round(connection)

    def lock_run_round(self, connection):
        self.game_running = True
        self.get_questions_and_run_round(connection)
        self.game_running = False

    def get_questions_and_run_round(self, connection):
        csv = Trivia_Set(self.csv_filename, self.log)
        if not csv.error:
            self.run_round(connection, csv)

    def run_round(self, connection, csv):
        questions = csv.get_questions()
        game = Game(questions, connection, self.record, self.players)
        game.go()
