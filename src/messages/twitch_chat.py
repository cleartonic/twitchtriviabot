import random

class Chat:
    good_morning = 'Refactored out of a cleartonic fork by @LtJG_Bodhi_Cooper: Trivvy Bot V-2.0 has been called into existence.'
    good_night = 'Trivvy Bot V-2.0 has business in a parrallel dimension. Bye for now!'

    new_game_catchphrase = [
        "Aaaah let's get ready to rumble!",
        "Y'all ready for this?",
        "Let's get this party started!"
    ]

    new_round = "Ok, time to get this round started."

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

    def four_way_tie(players):
        pass

    def five_way_tie(players):
        pass

    def draw_the_board(players):
        pass

    def new_game(top_players):
        return random.choice(Chat.new_game_catchphrase)

    def end_game(game_winners):
        "This is when another bot might say who won. I'll leave that up to the bot commander for now..."

    def end_round(round_winners):
        "So that's the round. I could tell you who's winning, but I don't feel like it right now."
