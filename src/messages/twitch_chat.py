import random
from string import Template

class Chat:
    good_morning = 'Refactored out of a cleartonic fork by @LtJG_Bodhi_Cooper: Trivvy Bot V-2.0 has been called into existence.'
    good_night = 'Trivvy Bot V-2.0 has business in a parrallel dimension. Bye for now!'

    new_game_catchphrase = [
        "Aaaah let's get ready to rumble!",
        "Y'all ready for this?",
        "Let's get this party started!"
    ]

    end_game_signoff = [
        "And that's the game! Here's who won:",
        "Drum roll please for the winners:",
        "We have our trivvy champions:"
    ]

    new_round_catchphrase = [
        Template("Ok, time to get round $name started."),
        Template("Round $name => FIGHT!")
    ]

    end_round_conclusion = [
        "That's the end of this round. Leaders:",
        "Here are the leaders at the end of this round:"
    ]

    no_scores = [
        "I'd tell you who is winning, but no one has scored",
        "Are you even playing? Because I got no scores.",
        "You miss 100% of the shots you don't take. No scores yet..."
        "man. these must be some hard questions. No one's gotten any of it right."
    ]

    sole_score = [
        "Look there was only one person who scored so guess what they get the gold."
    ]

    all_way_tie = [
        "There may be more who tied, but I can only keep track of three."
    ]

    tie_for_two = [
        "What do you know, it's a big tie!"
    ]

    tie_for_gold = [
        "It's a tie for gold!"
    ]

    unanswered_questions = [
        "Let's just move on, shall we?",
        "Ok, so that was a non-starter",
        "Wow. No one knows?",
        "Anyone? Anyone? Bueller? Moving on -",
        "... we'll just chalk that one up to beeing poorly worded."
    ]

    def player(name, points):
        return f"{name}: {points}pts"

    def join_players(players):
        names, scores = zip(*players)
        return (" & ".join(names), scores[0])

    def gold(player):
        player = Chat.player(player[0], player[1])
        return f"*<==={player}===>*"

    def silver(player):
        player = Chat.player(player[0], player[1])
        return f"=={player}=="

    def bronze(player):
        player = Chat.player(player[0], player[1])
        return f"={player}="

    def none_played():
        return random.choice(Chat.no_scores)

    def one_player(players):
        winner = Chat.gold(players[0])
        comment = random.choice(Chat.sole_score)
        return f"{comment} {winner}"

    def two_players(players):
        gold = Chat.gold(players[0])
        silver = Chat.silver(players[1])
        return f"{gold} | {silver}"

    def two_person_two_way_tie(players):
        tied_players [players[0], players[1]]
        winners = Chat.gold(Chat.join_players(tied_players))
        comment = random.choice(Chat.tie_for_two)
        return f"{comment} {winners}"

    def no_tie_game(players):
        gold = Chat.gold(players[0])
        silver = Chat.silver(players[1])
        bronze = Chat.bronze(players[2])
        return f"{gold} | {silver} | {bronze}"

    def three_person_two_way_gold_tie(players):
        tied_players = [players[0], players[1]]
        gold = Chat.gold(Chat.join_players(tied_players))
        silver = chat.silver(players[2])
        winners = f"{gold} | {silver}"
        comment = random.choice(Chat.tie_for_gold)
        return f"{comment} {winners}"

    def three_person_two_way_silver_tie(players):
        tied_players = [players[1], players[2]]
        gold = Chat.gold(players[1])
        silver = chat.silver(Chat.join_players(tied_players))
        return f"{gold} | {silver}"

    def three_way_tie(players):
        tied_players [players[0], players[1], players[2]]
        winners = Chat.gold(Chat.join_players(tied_players))
        comment = random.choice(Chat.all_way_tie)
        return f"{comment} {winners}"

    def format_leader_board(players):
        if len(players) == 0:
            return Chat.none_played()
        elif len(players) == 1:
            return Chat.one_player(players)
        elif len(players) == 2:
            if players[0][1] == players[1][1]:
                return Chat.two_person_two_way_tie(players)
            return Chat.two_players(players)
        elif players[0][1] == players[2][1]:
            return Chat.three_way_tie(players)
        elif players[0][1] == players[1][1]:
            return Chat.three_person_two_way_gold_tie(players)
        elif players[1][1] == players[2][1]:
            return Chat.three_person_two_way_silver_tie(players)
        return Chat.no_tie_game(players)

    def new_round(round_name):
        return random.choice(Chat.new_round_catchphrase).substitute(name=round_name)

    def end_round(round_winners):
        saying = random.choice(Chat.end_round_conclusion)
        winners = Chat.format_leader_board(round_winners)
        return f"{saying} {winners}"

    def new_game(top_players):
        saying = random.choice(Chat.new_game_catchphrase)
        winners = Chat.format_leader_board(top_players)
        return f"{saying} {winners}"

    def end_game(game_winners):
        saying = random.choice(Chat.end_game_signoff)
        winners = Chat.format_leader_board(game_winners)
        return f"{saying} {winners}"
