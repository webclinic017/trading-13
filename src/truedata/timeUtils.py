import os
import sys
from datetime import datetime as d

class timeUtils:
    def __init__(self):
        pass

    def check_if_current_time_is_end_of_minute(self):
        current_time = d.now()
        current_time_in_seconds = current_time.strftime("%S")
        #print("\r" + current_time_in_seconds)
        sys.stdout.write('\r' +  "Seconds: " + str(current_time_in_seconds))
        if current_time_in_seconds == "01":
            return True
        else:
            return False

    def check_if_current_time_is_end_of_five_minutes(self):
        current_time = d.now()
        current_time_in_seconds = current_time.strftime("%M")
        #print(current_time_in_seconds)
        if int(current_time_in_seconds)%5 == 0:
            return True
        else:
            return False
