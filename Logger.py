import os
from datetime import datetime

class Logger(object):

    def __init__(self, file = 'scanner_log.txt'):
        self.file = str(file)

    def add(self, data):

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file), mode='a') as log_file:
            log_file.write(datetime.strftime(datetime.now(), "%c") + " " + str(data) + "\n" )


