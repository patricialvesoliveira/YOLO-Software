import RPi.GPIO as GPIO
from Core.Enumerations import *

PIN_TOUCH = 16

class TouchSensor:

    def __init__(self):
        self.sensorType = SensorType.TOUCH
        self.state = TouchState.NOT_TOUCHING

        # set up pins
        if GPIO.getmode() is not GPIO.BCM:
            raise Exception("Error: The GPIO mode is different that the one the touch sensor uses (BCM numbering)")
        GPIO.setup(PIN_TOUCH, GPIO.IN)
        print "OK! -- Touch sensor set up!"
        return

    def update(self):

        if not GPIO.input(PIN_TOUCH):
            self.state = TouchState.TOUCHING
        else:
            self.state = TouchState.NOT_TOUCHING

    def getState(self):
        return self.state
