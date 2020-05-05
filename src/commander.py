class Commander:
    commands = [
        "!triviastart",
        "!triviastartround",
        "!nextround",
        "!triviaend",
        "!top3"
    ]

    def __init__(self, admins, commands):
        pass

    def parse_if_command(reply):
        username = reply[0]
        message = reply[1]
        pass

    def load_trivia():
        pass # what if this is just checked when trivia is started?

    def start_game(username):
        pass

    def start_round(username):
        pass

    def next_round(username):
        pass

    def end_game(username):
        pass

    def leaderBoard(username):
        pass

    def hint(username):
        pass

    def backup_trivia():
        pass # what if this is just auto-backed up?
