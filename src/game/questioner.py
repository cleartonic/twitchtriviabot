import re

class Questioner:
    hint_replacement = '_'

    def clean(answer):
        lower_case = answer.lower()
        letters_only = filter(str.isalpha, lower_case)
        return "".join(letters_only)

    def __init__(self, question, connection):
        self.ask = question['Ask']
        self.answer = question['Answer']
        self.connection = connection

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        self.connection.send(self.ask)

    def run(self):
        pass

    def end(self):
        pass

    def check_answer(self, participant_answer):
        participant_answer = Questioner.clean(participant_answer)
        correct_answer = Questioner.clean(self.answer)
        return correct_answer in participant_answer

    def first_hint(self):
        hint = ""
        for index, char in enumerate(self.answer):
            hint += char if index % 3 == 0 else Questioner.hint_replacement
        return hint

    def second_hint(self):
        vowels = '[aeiou]'
        repl = Questioner.hint_replacement
        return re.sub(vowels, repl, self.answer, flags=re.I)
