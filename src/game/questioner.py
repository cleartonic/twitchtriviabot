import re
import random
from src.messages import Chat

class Questioner:
    hint_replacement = '_'

    def clean(answer):
        lower_case = answer.lower()
        letters_only = filter(str.isalpha, lower_case)
        return "".join(letters_only)

    def __init__(self, question, connection, game_record):
        self.question = question
        self.ask = question['Ask']
        self.answer = question['Answer']
        self.connection = connection
        self.game_record = game_record

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        self.connection.send(self.ask)

    def run(self):
        pass

    def end(self):
        self.game_record.log(self.question)
        self.connection.send(random.choice(Chat.unanswered_questions))

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
