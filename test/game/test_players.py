import unittest
import os
from src.game.players import Players as Subject

class PlayersTestCase(unittest.TestCase):
    def cleanup(self, filename):
        if os.path.exists(f"{filename}.txt"):
          os.remove(f"{filename}.txt")

    def test_players_score_adds_new_players_to_the_board(self):
        player = "paul2D2"
        expected = {
            "round_points": 1,
            "game_points": 1,
            "game_wins": 0
        }
        filename = "mock_players"
        s = Subject(filename)

        s.score(player)

        self.cleanup(filename)
        self.assertEqual(s.scores[player], expected)

    def test_players_score_ups_an_existing_players_score(self):
        player = "paul2D2"
        expected = {
            "round_points": 2,
            "game_points": 2,
            "game_wins": 0
        }
        filename = "mock_players"
        s = Subject(filename)

        s.score(player)
        s.score(player)

        self.cleanup(filename)
        self.assertEqual(s.scores[player], expected)

    def test_players_winner_adds_a_game_win_to_a_player_on_the_board(self):
        winners = [ "paul2D2" ]
        expected = {
            winners[0]: {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 1
            }
        }
        filename = "mock_players"
        s = Subject(filename)
        s.score(winners[0])

        s.score_winners(winners)

        self.cleanup(filename)
        self.assertEqual(s.scores, expected)

    def test_players_winner_only_adds_a_game_win_to_players_on_the_board(self):
        winners = [ "paul2D2", "biggs_darklighter" ]
        expected = {
            winners[0]: {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 1
            }
        }
        filename = "mock_players"
        s = Subject(filename)
        s.score(winners[0])

        s.score_winners(winners)

        self.cleanup(filename)
        self.assertEqual(s.scores, expected)

    def test_players_winner_adds_a_game_win_to__multiple_players_on_the_board(self):
        winners = [ "paul2D2", "biggs_darklighter" ]
        expected = {
            winners[0]: {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 1
            },
            winners[1]: {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 1
            }
        }
        filename = "mock_players"
        s = Subject(filename)
        s.score(winners[0])
        s.score(winners[1])

        s.score_winners(winners)

        self.cleanup(filename)
        self.assertEqual(s.scores, expected)

    def test_players_new_round_clears_all_old_round_scores(self):
        players = [ "paul2D2", "biggs_darklighter" ]
        expected = {
            players[0]: {
                "round_points": 0,
                "game_points": 1,
                "game_wins": 1
            },
            players[1]: {
                "round_points": 0,
                "game_points": 2,
                "game_wins": 1
            }
        }
        filename = "mock_players"
        s = Subject(filename)
        s.score(players[0])
        s.score(players[1])
        s.score(players[1])
        s.score_winners(players)

        s.reset_scores_for_next_round()

        self.cleanup(filename)
        self.assertEqual(s.scores, expected)

    def test_players_new_game_clears_all_old_round_and_game_scores(self):
        players = [ "paul2D2", "biggs_darklighter" ]
        expected = {
            players[0]: {
                "round_points": 0,
                "game_points": 0,
                "game_wins": 1
            },
            players[1]: {
                "round_points": 0,
                "game_points": 0,
                "game_wins": 1
            }
        }
        filename = "mock_players"
        s = Subject(filename)
        s.score(players[0])
        s.score(players[1])
        s.score(players[1])
        s.score_winners(players)

        s.reset_scores_for_next_game()

        self.cleanup(filename)
        self.assertEqual(s.scores, expected)

    def skip_test_players_round_winners_gives_the_top_3_round_players(self):
        pass

    def skip_test_players_game_winners_gives_the_top_3_game_players(self):
        pass

    def test_players_top_players_gives_the_top_3_players(self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k", ]
        expected = [
            (players[3], 5),
            (players[4], 4),
            (players[1], 3)
        ]
        filename = "mock_players"
        s = Subject(filename)
        for player in players:
            s.score(player)
        s.score_winners([ players[3] ])
        s.score_winners([ players[4], players[3] ])
        s.score_winners([ players[1], players[4], players[3] ])
        s.score_winners([ players[0], players[1], players[4], players[3] ])
        s.score_winners([ players[2], players[0], players[1], players[4], players[3] ])

        actual = s.top_players()

        self.cleanup(filename)
        self.assertEqual(expected, actual)
        pass
