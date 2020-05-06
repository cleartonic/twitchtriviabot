class Questioner:
    def clean(answer):
        return "".join(answer.split())

    def __init__(self, question):
        self.ask = question['Ask']
        self.answer = Questioner.clean(question['Answer'])

    def ask_text(self):
        return self.ask

    def check_answer(self, participant_answer):
        answer = "".join(participant_answer.split())
        return answer == self.answer
