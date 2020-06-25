from mocks.game.game_record import Game_Record
from mocks.game.players import Players

from .go import Go
from .stop import stop

class all:
    def commands():
        return [
            Go('triviaset.csv', Game_Record(), Players()).tuple(),
            stop.tuple(),
        ]
