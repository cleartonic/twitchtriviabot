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
        winners = [ "paul2D2", "duncan_idaho" ]
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
        winners = [ "paul2D2", "gurney" ]
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
        players = [ "paul2D2", "barron_harkonnen" ]
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
        players = [ "paul2D2", "the_great_worm" ]
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

    def test_players_round_winners_gives_the_top_3_round_players(self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k" ]
        expected = [
            (players[3], 5),
            (players[4], 4),
            (players[1], 3)
        ]
        filename = "mock_players"
        s = Subject(filename)
        for _ in range(5):
            s.score(players[3])
        for _ in range(4):
            s.score(players[4])
        for _ in range(3):
            s.score(players[1])
        for _ in range(2):
            s.score(players[0])
        s.score(players[2])

        actual = s.round_winners()

        self.cleanup(filename)
        self.assertEqual(expected, actual)

    def test_players_game_winners_gives_the_top_3_game_players(self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k" ]
        expected = [
            (players[3], 5),
            (players[4], 4),
            (players[1], 3)
        ]
        filename = "mock_players"
        s = Subject(filename)
        for _ in range(5):
            s.score(players[3])
        for _ in range(4):
            s.score(players[4])
        for _ in range(3):
            s.score(players[1])
        for _ in range(2):
            s.score(players[0])
        s.score(players[2])

        actual = s.game_winners()

        self.cleanup(filename)
        self.assertEqual(expected, actual)

    def test_players_top_players_gives_the_top_3_players(self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k" ]
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

    def test_players_top_players_gives_first_3_players_to_get_on_the_board_when_there_are_many (self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k" ]
        expected = [
            (players[0], 1),
            (players[1], 1),
            (players[2], 1)
        ]
        filename = "mock_players"
        s = Subject(filename)
        for player in players:
            s.score(player)
        s.reset_scores_for_next_game
        s.score_winners([ players[2], players[0], players[1], players[4], players[3] ])

        actual = s.top_players()

        self.cleanup(filename)
        self.assertEqual(expected, actual)

    def test_players_top_players_gives_2_players_when_there_are_only_2 (self):
        players = [ "paul2D2", "macready_13" ]
        expected = [
            (players[1], 2),
            (players[0], 1)
        ]
        filename = "mock_players"
        s = Subject(filename)
        for player in players:
            s.score(player)
        s.reset_scores_for_next_game
        s.score_winners([ players[1] ])
        s.score_winners([ players[0], players[1] ])

        actual = s.top_players()

        self.cleanup(filename)
        self.assertEqual(expected, actual)

    def test_players_top_players_gives_the_only_player_whose_played (self):
        players = [ "paul2D2" ]
        expected = [
            (players[0], 1)
        ]
        filename = "mock_players"
        s = Subject(filename)
        for player in players:
            s.score(player)
        s.reset_scores_for_next_game
        s.score_winners([ players[0] ])

        actual = s.top_players()

        self.cleanup(filename)
        self.assertEqual(expected, actual)

    def test_players_top_players_gives_noting_if_no_one_has_played (self):
        players = [ "paul2D2" ]
        expected = []
        filename = "mock_players"
        s = Subject(filename)
        for player in players:
            s.score(player)
        s.reset_scores_for_next_game

        actual = s.top_players()

        self.cleanup(filename)
        self.assertEqual(expected, actual)
