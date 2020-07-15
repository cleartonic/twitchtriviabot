class Players():
    def __init__(self, filename):
        self.filename = f"{filename}.txt"
        self.mock_scores = {
            "trivvy_fan": {
                "round_points": 4,
                "game_points": 4,
                "game_wins": 2
            },
            "happy_lass": {
                "round_points": 6,
                "game_points": 12,
                "game_wins": 5
            }
        }

    def score(self, player):
        if player in self.mock_scores.keys():
            self.up_score(player)
        else:
            self.add_to_board(player)

    def up_score(self, player):
        self.mock_scores[player]['round_points'] += 1
        self.mock_scores[player]['game_points'] += 1

    def add_to_board(self, player):
        self.mock_scores[player] = {
            "round_points": 1,
            "game_points": 1,
            "game_wins": 0
        }

    def score_winners(self):
        players = self.game_winners()
        for player in players:
            if player in self.mock_scores.keys():
                self.mock_scores[player]["game_wins"] += 1

    def reset_scores_for_next_round(self):
        self.reset("round_points")

    def reset_scores_for_next_game(self):
        self.reset("round_points")
        self.reset("game_points")

    def reset(self, thing_to_be_reset):
        for score in self.mock_scores.values():
            score[thing_to_be_reset] = 0

    def round_winners(self):
        pass

    def game_winners(self):
        pass

    def top_players(self):
        pass
