class Time:

    def __init__(self, log):
        self.log = log

    def sleep(self, number):
        self.log(f'slept for {number} second(s)')
