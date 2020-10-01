import datetime

class Alarm:

    def __init__(self):
        self.active = False

    def set_alarm(self, month, day, hrs, min):
        self.alarmtime = datetime.datetime(2020, month, day, hrs, min)
        print("Alarm set")
        self.active = True

    def alarm_active(self):
        return self.active

    def check_alarm(self):
        if datetime.datetime.now() >= self.alarmtime:
            self.active = False
            return True
        else:
            return False
