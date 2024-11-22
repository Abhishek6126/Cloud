# utils/helpers.py

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        # Clear the log file at the start
        with open(self.log_file, 'w') as f:
            f.write('')

    def log(self, message):
        print(message)
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')
