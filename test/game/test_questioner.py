import unittest
from mocks.connection import Connection
from src.game.questioner import Questioner as Subject

class QuestionerTestCase(unittest.TestCase):
    def test_questioner_knows_itself_and_expects_strings_as_input(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        s = Subject(question, connection)
        self.assertEqual(s.ask, "What's a Diorama?")
        self.assertEqual(type(s.ask), str)
        self.assertEqual(type(s.ask), str)


    def test_questioner_doesnt_care_if_there_are_extra_fields(self):
        question = {
            'Round': 1,
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!",
            'Answer2': 'D\'oh!'
        }
        connection = Connection()
        Subject(question, connection)

    def test_questioner_gives_its_ask(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        subject = Subject(question, connection).ask
        self.assertEqual(subject, "What's a Diorama?")

    def test_questioner_identifies_an_exact_correct_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        participant_answer = "OMG Han! Chewie! They're all here!"
        subject = Subject(question, connection).check_answer(participant_answer)
        self.assertEqual(subject, True)

    def test_questioner_identifies_an_incorrect_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        participant_answer = "I don't know, some kind of goblin-man."
        subject = Subject(question, connection).check_answer(participant_answer)
        self.assertEqual(subject, False)

    def test_questioner_identifies_a_correct_answer_with_extra_whitespace(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        participant_answer = " \t \rOMG Han! Chewie! They're all here!\r \n "
        subject = Subject(question, connection).check_answer(participant_answer)
        self.assertEqual(subject, True)

    def test_questioner_identifies_a_correct_answer_ignoring_internal_whitespace(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        participant_answer = " \t \rOMGHan!   Chewie! \t They're all here!\r \n "
        subject = Subject(question, connection).check_answer(participant_answer)
        self.assertEqual(subject, True)

    def test_questioner_identifies_a_correct_answer_ignoring_case(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        participant_answer = "OmG hAn! CheWIe! theY're all hEre!"
        subject = Subject(question, connection).check_answer(participant_answer)
        self.assertEqual(subject, True)

    def test_questioner_identifies_a_correct_answer_inside_a_message(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        participant_answer = "I would say OMG Han! Chewie! They're all here! what do you think?"
        subject = Subject(question, connection).check_answer(participant_answer)
        self.assertEqual(subject, True)

    def test_questioner_identifies_an_exact_correct_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        participant_answer = "O!M@G#H$a%n^?&C*(h)e_w-i+e=!{T}[h]e|y'r\\e:a;l\"l'<h>e,r.e/"
        subject = Subject(question, connection).check_answer(participant_answer)
        self.assertEqual(subject, True)

    def test_questioner_first_hint_returns_2_out_of_3_chars_in_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        subject = Subject(question, connection).first_hint()
        self.assertEqual(subject, "O__ __n__C__w__!__h__'__ __l__e__!")

    def test_questioner_second_hint_returns_no_vowels_in_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        subject = Subject(question, connection).second_hint()
        self.assertEqual(subject, "_MG H_n! Ch_w__! Th_y'r_ _ll h_r_!")

    def test_questioner_asks_a_question_to_the_chat_to_start(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        connection = Connection()
        Subject(question, connection).start()
        self.assertEqual(connection.message, "What's a Diorama?")
