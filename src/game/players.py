import os

class Players():
    def __init__(self, filename):
        self.filename = f"{filename}.txt"
        self.cache = None
        self.scores = self.get_scores_from_FS()

    def score(self, player):
        self.get_scores()
        if player in self.scores.keys():
            self.up_score(player)
        else:
            self.add_to_board(player)
        self.save_scores()

    def up_score(self, player):
        self.scores[player]['round_points'] += 1
        self.scores[player]['game_points'] += 1

    def add_to_board(self, player):
        self.scores[player] = {
            "round_points": 1,
            "game_points": 1,
            "game_wins": 0
        }

    def score_winners(self, winners):
        self.get_scores()
        for player in winners:
            # pretty sure it's impossible for someone to win and not be on the board
            if player in self.scores.keys(): 
                self.scores[player]["game_wins"] += 1
        self.save_scores()

    def reset_scores_for_next_round(self):
        self.get_scores()
        self.reset("round_points")
        self.save_scores()

    def reset_scores_for_next_game(self):
        self.get_scores()
        self.reset("round_points")
        self.reset("game_points")
        self.save_scores()

    def reset(self, thing_to_be_reset):
        for score in self.scores.values():
            score[thing_to_be_reset] = 0

    def round_winners(self):
        pass

    def game_winners(self):
        pass

    def top_players(self):
        return self.top_3_by("game_wins")

    def top_3_by(self, point_type):
        player_tuples = []
        for player, record in self.scores.items():
            player_tuples.append((player, record[point_type]))
        sorted_players = sorted(player_tuples, key=lambda player: player[1], reverse=True)
        return sorted_players[:3]

    def get_scores(self):
        self.scores = self.get_scores_from_FS()

    def save_scores(self):
        self.overwrite_scores_to_FS()

    def get_scores_from_FS(self):
        blank_scores = {}
        if self.cache or self.cache == blank_scores:
            return self.cache

        if os.path.exists(self.filename):
            return self.read_from_existing_record()

        self.scores = blank_scores
        self.save_scores()
        self.cache = blank_scores
        return blank_scores

    def read_from_existing_record(self):
        file = open(self.filename)
        scores = eval(file.read())
        self.cache = scores
        file.close()
        return scores

    def overwrite_scores_to_FS(self):
        file = open(self.filename, "wt")
        file.write(str(self.scores))
        self.clear_score_cache()
        file.close()

    def clear_score_cache(self):
        self.cache = None
