from mocks.game.timer import Timer
from src.messages import Chat
from src.game.questioner import Questioner

class Round():

    def __init__(self, questions, connection, game_record, players):
        self.name = questions[0]['Round'] if questions else 0
        self.connection = connection
        self.game_record = game_record
        self.timer = Timer()
        self.players = players
        self.questioners = self.init_questioners(questions)

    def init_questioners(self, questions):
        return [self.init_q(question) for question in questions]

    def init_q(self, question):
        return Questioner(question, self.connection, self.game_record, self.timer)

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        self.connection.send(Chat.new_round(self.name))

    def run(self):
        for questioner in self.questioners:
            questioner.go()

    def end(self):
        self.connection.send(Chat.end_round(self.players.round_winners()))
        self.players.reset_scores_for_next_round()
