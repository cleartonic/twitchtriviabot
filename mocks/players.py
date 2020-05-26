class Players():
    def __init__(self):
        self._score = "Not Yet Called."
        self._winner = "Not Yet Called."
        self._new_round_called = False
        self._new_game_called = False
        self._round_winners = [
            ("Round_GoldPlayer", 5),
            ("Round_SilverPlayer", 4),
            ("Round_BronzePlayer", 3)
        ]
        self._game_winners = [
            ("Game_GoldPlayer", 5),
            ("Game_SilverPlayer", 4),
            ("Game_BronzePlayer", 3)
        ]
        self._top_players = [
            ("Top_GoldPlayer", 5),
            ("Top_SilverPlayer", 4),
            ("Top_BronzePlayer", 3)
        ]

    def score(self, player):
        self._score = player

    def winner(self):
        self._winner = self._game_winners[0][0]

    def new_round(self):
        self._new_round_called = True

    def new_game(self):
        self._new_game_called = True

    def round_winners(self):
        return self._round_winners

    def game_winners(self):
        return self._game_winners

    def top_players(self):
        return self._top_players
