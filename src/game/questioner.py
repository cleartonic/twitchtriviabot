class Questioner:
    def clean(answer):
        lower_case = answer.lower()
        letters_only = (x for x in lower_case if x.isalpha())
        return "".join(letters_only)

    def __init__(self, question):
        self.ask = question['Ask']
        self.answer = Questioner.clean(question['Answer'])

    def ask_text(self):
        return self.ask

    def check_answer(self, participant_answer):
        answer = Questioner.clean(participant_answer)
        return self.answer in answer
