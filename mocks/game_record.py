class Game_Record():
    def __init__(self):
        self.mock_log = [ ]
        self.clear_received = False

    def log(self, question):
        self.mock_log.append(question)

    def clear_game(self):
        self.clear_received = True
