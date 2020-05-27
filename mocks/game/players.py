class Players():
    def __init__(self):
        self._score = "Not Yet Called."
        self._winner = "Not Yet Called."
        self._next_round_called = "Round did not tell Players to reset the Round Scores"
        self._next_game_called = "Game did not tell Players to reset the Game Scores"
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

    def score_winners(self):
        self._winner = self._game_winners[0][0]

    def reset_scores_for_next_round(self):
        self._next_round_called = "Round Scores Reset"

    def reset_scores_for_next_game(self):
        self._next_game_called = "Game Scores Reset"

    def round_winners(self):
        return self._round_winners

    def game_winners(self):
        return self._game_winners

    def top_players(self):
        return self._top_players
