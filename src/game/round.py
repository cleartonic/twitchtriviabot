from mocks.game.game_record import Game_Record
from mocks.game.timer import Timer
from src.messages import Chat

class Round():

    def __init__(self, questioner, questions, connection, players):
        self.name = questions[0]['Round'] if questions else 0
        self.questioner = questioner
        self.connection = connection
        self.game_record = Game_Record()
        self.timer = Timer()
        self.players = players
        self.questioners = self.init_questioners(questions)

    def init_questioners(self, questions):
        return [self.init_q(question) for question in questions]

    def init_q(self, question):
        return self.questioner(question, self.connection, self.game_record, self.timer)

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        self.connection.send(Chat.new_round(self.name))

    def run(self):
        pass

    def end(self):
        self.connection.send(Chat.end_round(self.players.round_winners()))
        self.players.reset_scores_for_next_round()
