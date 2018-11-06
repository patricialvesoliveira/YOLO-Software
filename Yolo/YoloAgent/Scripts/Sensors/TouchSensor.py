import RPi.GPIO as GPIO
from Libs.Constants import *

PIN_TOUCH = 16


class TouchSensor:

    def __init__(self):
        self.sensorType = SensorType.TOUCH
        self.touchState = TouchState.NOT_TOUCHING

        # set up pins
        if GPIO.getmode() is not GPIO.BCM:
            raise Exception("Error: The GPIO mode is different that the one the touch sensor uses (BCM numbering)")

        GPIO.setup(PIN_TOUCH, GPIO.IN)

        print "OK! -- Touch sensor set up!"
        return

    def recordTouchInput(self):

        if GPIO.input(PIN_TOUCH) == 0:
            self.touchState =  TouchState.TOUCHING
        else:
            self.touchState =  TouchState.NOT_TOUCHING

        return (self.sensorType, self.touchState)
