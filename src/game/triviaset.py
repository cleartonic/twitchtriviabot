import pandas
import math
from src.messages import Log as report

class Trivia_Set:
    required_columns = ['Round', 'Ask', 'Answer']

    def __init__(self, csv_file, log = print):
        dataFrame = pandas.read_csv(csv_file)
        self.log = log
        self.columns = dataFrame.to_dict()
        self.error = self.validate_columns(self.columns)
        self.questions = dataFrame.to_dict('record')

    def validate_columns(self, columns):
        for column in Trivia_Set.required_columns:
            for key, value in columns[column].items():
                if type(value) != str and math.isnan(value):
                    message = f'It looks like there\'s an empty {column} on question { key + 1 } in the triviaset file'
                    self.log(report.question_load_problem(message))
                    return True

    def get_questions(self):
        return self.questions
