class Round():
    def __init__(self, questioner, questions):
        self.questioners = [questioner(question) for question in questions]

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
