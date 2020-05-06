import unittest
from src.game.questioner import Questioner as Subject

class QuestionerTestCase(unittest.TestCase):
    def test_questioner_knows_itself(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(question)
        self.assertEqual(s.ask, "What's a Diorama?")
        self.assertEqual(s.answer, "OMG Han! Chewie! They're all here!")

    def test_questioner_accepts_arbitrary_values_since_its_validated_elsewhere(self):
        question = {
            'Ask': 24601,
            'Answer': False
        }
        s = Subject(question)
        self.assertEqual(s.ask, 24601)
        self.assertEqual(s.answer, False)


    def test_questioner_doesnt_care_if_there_are_extra_fields(self):
        question = {
            'Round': 1,
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!",
            'Answer2': 'D\'oh!'
        }
        Subject(question)

    def test_questioner_gives_its_ask(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        subject = Subject(question).ask_text()
        self.assertEqual(subject, "What's a Diorama?")

    def test_questioner_identifies_an_exact_correct_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        participant_answer = "OMG Han! Chewie! They're all here!"
        subject = Subject(question).check_answer(participant_answer)
        self.assertEqual(subject, True)

    def test_questioner_identifies_an_incorrect_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        participant_answer = "I don't know, some kind of goblin-man."
        subject = Subject(question).check_answer(participant_answer)
        self.assertEqual(subject, False)

    def test_questioner_identifies_a_correct_answer_with_extra_whitespace(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        participant_answer = " \t \rOMG Han! Chewie! They're all here!\r \n "
        subject = Subject(question).check_answer(participant_answer)
        self.assertEqual(subject, True)
