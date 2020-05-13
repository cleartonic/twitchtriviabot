class Game_Record():
    def __init__(self):
        self.mock_log = [ ]

    def log(self, question):
        self.mock_log.append(question)
