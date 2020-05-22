class Players():
    def __init__(self):
        self._score = "Not Yet Called."
        self._winner = "Not Yet Called."
        self._new_round_called = False
        self._new_game_called = False
        self._round_winners = [
            ("Round_GoldPlayer", 5),
            ("Round_SilverPlayer", 4),
            ("Round_BronzePlayer", 3),
            ("Round_CopperPlayer", 2),
            ("Round_IronPlayer", 1)
        ]
        self._game_winners = [
            ("Game_GoldPlayer", 5),
            ("Game_SilverPlayer", 4),
            ("Game_BronzePlayer", 3),
            ("Game_CopperPlayer", 2),
            ("Game_IronPlayer", 1)
        ]
        self._top_players = [
            ("Top_GoldPlayer", 5),
            ("Top_SilverPlayer", 4),
            ("Top_BronzePlayer", 3),
            ("Top_CopperPlayer", 2),
            ("Top_IronPlayer", 1)
        ]

    def score(self, player):
        self.score = player

    def winner(self, player):
        self.winner = player

    def new_round(self):
        self.new_round_called = True

    def new_game(self):
        self.new_game_called = True

    def round_winners(self):
        return self._round_winners

    def game_winners(self):
        return self._game_winners

    def top_players(self):
        return self._top_players
