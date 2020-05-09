class Questioner:

    def mock(did_they_get_it_right):
        return Questioner(did_they_get_it_right)

    def __init__(self, did_they_get_it_right):
        self.ask = "Where now are the snow dens of yesteryear?"
        self.did_they_get_it_right = did_they_get_it_right

    def check_answer(self, participant_answer):
        return self.did_they_get_it_right

    def first_hint(self):
        return 'Not a real first hint'

    def second_hint(self):
        return 'Not a real second hint'
