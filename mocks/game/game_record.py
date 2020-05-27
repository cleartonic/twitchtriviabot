class Game_Record():
    def __init__(self):
        self._log = []
        self._clear_received = False

    def log(self, question):
        self._log.append(question)

    def clear_game(self):
        self._log = []
        self._clear_received = True

    def logged_questions(self):
        return self._log
