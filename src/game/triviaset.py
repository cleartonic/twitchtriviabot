import pandas
import math

class Trivia_Set:
    required_columns = ['Round', 'Ask', 'Answer']

    def __init__(self, csv_file):
        dataFrame = pandas.read_csv(csv_file)
        self.columns = dataFrame.to_dict()
        self.questions = dataFrame.to_dict('record')
        self.validate_columns(self.columns)
        self.validate_rounds(self.columns['Round'])

    def validate_columns(self, columns):
        for column in Trivia_Set.required_columns:
            for key, value in columns[column].items():
                if type(value) != str and math.isnan(value):
                    self.report_problem(f'It looks like there\'s an empty {column} on question { key + 1 } in the triviaset file')

    def validate_rounds(self, rounds):
        round_list = []
        for key, round in rounds.items():
            if type(round) != int:
                self.report_problem(f'It looks like at least one of the "Rounds" in the triviaset file is not an integer')
            if round not in round_list:
                round_list.append(round)
        round_list = sorted(round_list)
        if round_list[0] != 1:
            self.report_problem('It looks like either there are no questions in round 1 or you made a round 0 or something')
        if round_list[len(round_list) - 1] != len(round_list):
            self.report_problem('It looks like you skipped a round somewhere.')


    def report_problem(self, message):
        print('\n\tLuke, we\'ve got a malfunction in fire control...\n')
        print(message)
        print('Better go fix the triviaset.csv file before trying to shoot this thing off')
        exit()

    def get_questions(self):
        return self.questions
