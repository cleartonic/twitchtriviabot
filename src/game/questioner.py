class Questioner:
    def __init__(self, question):
        self.ask = question['Ask']
        self.answer = question['Answer']

    def ask_text(self):
        return self.ask

    def check_answer(self, participant_answer):
        answer = participant_answer.strip()
        return answer == self.answer
