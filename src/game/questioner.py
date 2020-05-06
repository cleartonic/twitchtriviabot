class Questioner:
    def __init__(self, question):
        self.ask = question['Ask']
        self.answer = question['Answer']

    def ask_text(self):
        return self.ask
