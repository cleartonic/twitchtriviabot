class Players():
    def __init__(self):
        self.mock_score = "Not Yet Called."
        self.mock_winner = "Not Yet Called."
        self.mock_new_round_called = False
        self.mock_new_game_called = False

    def score(self, player):
        self.mock_score = player

    def winner(self, player):
        self.mock_winner = player

    def new_round(self):
        self.mock_new_round_called = True

    def new_game(self):
        self.mock_new_game_called = True

    def round_winners(self):
        return [
            ("Round_GoldPlayer", 5),
            ("Round_SilverPlayer", 4),
            ("Round_BronzePlayer", 3),
            ("Round_CopperPlayer", 2),
            ("Round_IronPlayer", 1)
        ]

    def game_winners(self):
        return [
            ("Game_GoldPlayer", 5),
            ("Game_SilverPlayer", 4),
            ("Game_BronzePlayer", 3),
            ("Game_CopperPlayer", 2),
            ("Game_IronPlayer", 1)
        ]

    def top_players(self):
        [
            ("Top_GoldPlayer", 5),
            ("Top_SilverPlayer", 4),
            ("Top_BronzePlayer", 3),
            ("Top_CopperPlayer", 2),
            ("Top_IronPlayer", 1)
        ]
