from src.game.triviaset import Trivia_Set
from mocks.game.game_record import Game_Record
from mocks.game.players import Players
from src.game.game import Game

class Go:
    command = "!go"
    validate = [ "admin_only" ]

    def __init__(self, question_csv, game_record, players, log = print):
        self.csv_filename = question_csv
        self.record = game_record
        self.players = players
        self.log = log

    def tuple(self):
        return (Go.command, self.run_the_next_trivia_round, Go.validate)

    def run_the_next_trivia_round(self, connection, _message):
        csv = Trivia_Set(self.csv_filename, self.log)
        if not csv.error:
            questions = csv.get_questions()
            game = Game(questions, connection, self.record, self.players)
            game.go()
