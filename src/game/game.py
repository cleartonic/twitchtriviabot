from src.messages import Chat

class Game:

    def __init__(self, round, questioner, questions, connection, game_record):
        self.questioner = questioner
        self.round = round
        self.connection = connection
        self.game_record = game_record
        self.rounds = self.init_rounds(questions)

    def init_rounds(self, questions):
        game_questions = self.list_by_rounds(questions)
        return [self.init_r(round_questions) for round_questions in game_questions]

    def list_by_rounds(self, questions):
        round_questions = []
        for question in questions:
            if len(round_questions) == 0:
                round_questions.append([question])
            else:
                question_appended = False
                for round_set in round_questions:
                    if question['Round'] == round_set[0]['Round']:
                        round_set.append(question)
                        question_appended = True
                if not question_appended:
                    round_questions.append([question])
        return round_questions

    def init_r(self, round_questions):
        return self.round(self.questioner, round_questions, self.connection)

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        self.connection.send(Chat.new_game)

    def run(self):
        pass

    def end(self):
        self.game_record.clear_game()
        self.connection.send(Chat.end_game)
