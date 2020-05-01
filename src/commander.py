class Commander:
    commands = [
        "!triviastart",
        "!triviaend",
        "!top3",
        "!hint",
        "!bonus",
        "!score",
        "!next",
        "!stop",
        "!loadconfig",
        "!backuptrivia",
        "!loadtrivia",
        "!creator"
    ]

    def __init__(self, admins, commands):
        pass

    def parse_if_command(reply):
        username = reply[0]
        message = reply[1]
        pass

    def score():
        pass

    def leader_board():
        pass

    def useage():
        pass

    def stop_bot(username):
        pass

    def start_game(username):
        pass

    def next_round(username):
        pass

    def next_question(username):
        pass

    def end_game(username):
        pass

    def hint(username):
        pass

    def bonus(username):
        pass # how do you even use this?

    def load_config():
        pass # what if this always works?

    def backup_trivia():
        pass # what if this is just auto-backed up?

    def load_trivia():
        pass # what if this is just checked when trivia is started?
        # what if you can load the round this way?

    def creator():
        pass # how useful is this?
