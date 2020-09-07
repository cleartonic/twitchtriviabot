class Game_Record():
    def __init__(self):
        self._log = []

    def log(self, question):
        self._log.append(question)

    def clear_game(self):
        self._log = []

    def logged_questions(self):
        return self._log