import unittest
from src.game.players import Players as Subject

class PlayersTestCase(unittest.TestCase):
    def test_players_score_adds_new_players_to_the_board(self):
        player = "paul2D2"
        expected = {
            "round_points": 1,
            "game_points": 1,
            "game_wins": 0
        }
        s = Subject()

        s.score(player)

        self.assertEqual(s.mock_scores[player], expected)

    def test_players_score_ups_an_existing_players_score(self):
        player = "paul2D2"
        expected = {
            "round_points": 2,
            "game_points": 2,
            "game_wins": 0
        }
        s = Subject()

        s.score(player)
        s.score(player)

        self.assertEqual(s.mock_scores[player], expected)

    def skip_test_players_winner_adds_a_game_win_to_a_player(self):
        pass

    def skip_test_players_new_round_clears_all_old_round_scores(self):
        pass

    def skip_test_players_new_game_clears_all_old_round_scores(self):
        pass

    def skip_test_players_new_game_clears_all_old_game_scores(self):
        pass

    def skip_test_players_round_winners_gives_the_top_3_round_players(self):
        pass

    def skip_test_players_game_winners_gives_the_top_3_game_players(self):
        pass

    def skip_test_players_top_players_gives_the_top_3_round_players(self):
        pass
