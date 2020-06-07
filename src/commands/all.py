from .go import go
from .stop import stop

class all:
    def commands():
        return [
            go().tuple(),
            stop.tuple(),
        ]
