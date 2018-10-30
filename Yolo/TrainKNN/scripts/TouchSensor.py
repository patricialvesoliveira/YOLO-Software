import RPi.GPIO as GPIO

# Pin functions --- TODO - find out which pins in going to be used
PIN_TOUCH = 16


class TouchSensor:

    def __init__(self):

        # setting the GPIO mode that the board should
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_TOUCH, GPIO.IN)

        return

    def isBeingTouched(self):

        if GPIO.input(PIN_TOUCH) == 0:
            return True
        else:
            return False
