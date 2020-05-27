class Timer:

    def start_question_timer():
        self.times_asked = 0

    def question_time_up():
        self.times_asked += 1
        return self.times_asked >= 12

    def question_hint_1_up():
        return self.times_asked >= 4

    def question_hint_2_up():
        return self.times_asked >= 8
