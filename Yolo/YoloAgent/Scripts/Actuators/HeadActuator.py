import RPi.GPIO as GPIO
import os
import time
import numpy as np
from Libs.Constants import *

# Pin functions
PIN_MOTOR = 12 # PWM


class HeadActuator:

    def __init__(self):
        # set up pins
        if GPIO.getmode() is not GPIO.BCM:
            raise Exception("Error: The GPIO mode is different that the one the head motors use (BCM numbering)")

        # TODO --- remove all returns !!!!!!
        return

        # set up pins
        GPIO.setup(PIN_MOTOR, GPIO.OUT)  # pwm


        # set up PWM
        PWMfrequency = 50  # PWM frequency
        dutyCicle = 7.5  # duty cycle (2.5 (max speed Up), 7.5 (stop), 12.5 (maxspeed down) )
        self.motor = GPIO.PWM(PIN_MOTOR, PWMfrequency)
        self.motor.start(dutyCicle)

        print "OK! -- Head set up!"

        return

    def __del__(self):
        # TODO --- remove all returns !!!!!!
        return

        self.resetPinInput()

        print "Cleaning up head actuator"


    # Note: speed received varies between 0 - 100
    def moveTo(self, speed):


        print "Moving at " + str(speed) + "!"

        # TODO --- remove all returns !!!!!!
        return
        self.motor.ChangeDutyCycle(speed)  # changes motor 1 duty cycle (speed)

    def resetPinInput(self):
        # TODO --- remove all returns !!!!!!
        return

        self.motor.ChangeDutyCycle(0)

    def cleanupGPIOPins(self):
        # TODO --- remove all returns !!!!!!
        return
        try:
            self.motor.ChangeDutyCycle(0)
            GPIO.output(PIN_MOTOR, 0)
            self.motor.stop()

        except Exception:
            self.motor.ChangeDutyCycle(0)
            GPIO.output(PIN_MOTOR, 0)
            self.motor.stop()
            print("ERROR: There was a problem cleaning up the head actuator")

