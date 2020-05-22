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

    unanswered_questions = [
        "Let's just move on, shall we?",
        "Ok, so that was a non-starter",
        "Wow. No one knows?",
        "Anyone? Anyone? Bueller? Moving on -",
        "... we'll just chalk that one up to beeing poorly worded."
    ]

    def none_played(this_iteration):
        return f"I'd tell you who is winning, but no one has played {this_iteration}"

    def two_way_tie(players):
        pass

    def three_way_tie(players):
        pass

    def no_tie_game(players):
        gold = f"*<==={players[0][0]}: {players[0][1]}pts===>*"
        silver = f"=={players[1][0]}: {players[1][1]}pts=="
        bronze = f"={players[2][0]}: {players[2][1]}pts="
        return f"{gold} | {silver} | {bronze}"

    def format_leader_board(players):
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
