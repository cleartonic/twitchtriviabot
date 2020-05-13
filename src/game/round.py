from mocks.game_record import Game_Record

class Round():

    def __init__(self, questioner, questions, connection):
        self.questioner = questioner
        self.connection = connection
        self.game_record = Game_Record()
        self.questioners = self.init_questioners(questions)

    def init_questioners(self, questions):
        return [self.init_q(question) for question in questions]

    def init_q(self, question):
        return self.questioner(question, self.connection, self.game_record)

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        pass

    def run(self):
        pass

    def end(self):
        pass
