from src.messages import Chat

class Game:

    def __init__(self, round, questioner, questions, connection, game_record):
        self.questioner = questioner
        self.round = round
        self.connection = connection
        self.game_record = game_record
        self.rounds = self.init_rounds(questions)

    def init_rounds(self, questions):
        game_qs = self.list_by_rounds(questions)
        return [self.init_r(round_questions) for round_questions in game_qs]

    def init_r(self, round_questions):
        return self.round(self.questioner, round_questions, self.connection)

    def list_by_rounds(self, questions):
        game_qs = []
        for q in questions:
            self.add(q, game_qs) if game_qs else game_qs.append([q])
        return game_qs

    def add(self, question, game_questions):
        question_is_the_first_in_a_new_round = True
        for round_questions in game_questions:
            if question['Round'] == round_questions[0]['Round']:
                round_questions.append(question)
                question_is_the_first_in_a_new_round = False
        if question_is_the_first_in_a_new_round:
            game_questions.append([question])

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
