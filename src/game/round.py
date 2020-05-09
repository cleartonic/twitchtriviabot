class Round():
    def __init__(self, questioner, questions):
        self.questioners = [questioner(question) for question in questions]
