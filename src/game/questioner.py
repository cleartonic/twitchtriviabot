import re
import random
from src.messages import Chat
import time

class Questioner:
    hint_replacement = '_'

    def clean(answer):
        lower_case = answer.lower()
        letters_only = filter(str.isalpha, lower_case)
        return "".join(letters_only)

    def __init__(self, question, connection, game_record, timer):
        self.question = question
        self.ask = question['Ask']
        self.answer = question['Answer']
        self.connection = connection
        self.game_record = game_record
        self.timer = timer

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        self.connection.send(self.ask)

    def run(self):
        question_answered = False
        hint_1_given = False
        hint_2_given = False
        times_up = False
        self.timer.start_question_timer()
        while(not times_up and not question_answered):
            time.sleep(self.connection.seconds_per_message)
            response = self.connection.last_response
            if self.check_answer(response[1]):
                question_answered = True
                self.connection.send(Chat.correct_answer(response[0]))
            if not question_answered and not hint_2_given and self.timer.question_hint_2_up():
                hint_2_given = True
                self.connection.send(self.second_hint())
            elif not question_answered and not hint_1_given and self.timer.question_hint_1_up():
                hint_1_given = True
                self.connection.send(self.first_hint())
            times_up = self.timer.question_time_up()
        if not question_answered:
            self.connection.send(random.choice(Chat.unanswered_questions))

    def end(self):
        self.game_record.log(self.question)

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
