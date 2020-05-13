class Players():
    def __init__(self):
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
        if player in self.mockscores.keys():
            player['round_points'] += 1
            player['game_points'] += 1
        else:
            self.mock_scores[player] = {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 0
            }
