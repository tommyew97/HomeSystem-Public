from sense_hat import SenseHat

class PiHat():

    def __init__(self):
        pass
        self.sense = SenseHat()

    def buttonPress(self):
        pass
        for event in sense.stick.get_events():
            return event.direction