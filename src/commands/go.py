from src.game.triviaset import Trivia_Set
from mocks.game.game_record import Game_Record
from mocks.game.players import Players
from src.game.game import Game

class go:
    command = "!go"
    validate = [ "admin_only" ]

    def __init__(self):
        pass

    def tuple(self):
        return (go.command, self.run_the_next_trivia_round, go.validate)

    def run_the_next_trivia_round(self, connection, _message):
        csv = Trivia_Set("mocks/triviaset.csv") # 'triviaset.csv'
        if not csv.error:
            questions = csv.get_questions()
            game = Game(questions, connection, Game_Record(), Players())
            game.go()
