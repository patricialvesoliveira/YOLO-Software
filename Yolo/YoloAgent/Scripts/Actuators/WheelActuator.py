import RPi.GPIO as GPIO
import os
import time
import numpy as np
from Libs.Constants import *

# Pin functions
PIN_MOTOR1 = 19
PIN_MOTOR1_DIRECTION = 26
PIN_MOTOR2 = 17
PIN_MOTOR2_DIRECTION = 27
PIN_MOTOR3 = 20
PIN_MOTOR3_DIRECTION = 21


class WheelActuator:

    def __init__(self):
        # set up pins
        if GPIO.getmode() is not GPIO.BCM:
            raise Exception("Error: The GPIO mode is different that the one the wheel motors use (BCM numbering)")

        GPIO.setup(PIN_MOTOR1, GPIO.OUT)
        GPIO.setup(PIN_MOTOR1_DIRECTION, GPIO.OUT)

        GPIO.setup(PIN_MOTOR2, GPIO.OUT)
        GPIO.setup(PIN_MOTOR2_DIRECTION, GPIO.OUT)

        GPIO.setup(PIN_MOTOR3, GPIO.OUT)
        GPIO.setup(PIN_MOTOR3_DIRECTION, GPIO.OUT)

        # these just reverse directions
        GPIO.output(PIN_MOTOR1_DIRECTION, 0)
        GPIO.output(PIN_MOTOR3_DIRECTION, 0)
        GPIO.output(PIN_MOTOR2_DIRECTION, 0)

        # set up PWM
        PWMfrequency = 20  # PWM frequency, motor RPM = 5
        dutyCicle = 0  # duty cycle (0-100)
        self.motor1 = GPIO.PWM(PIN_MOTOR1, PWMfrequency)  # motor 1
        self.motor2 = GPIO.PWM(PIN_MOTOR2, PWMfrequency)  # motor 2
        self.motor3 = GPIO.PWM(PIN_MOTOR3, PWMfrequency)  # motor 3
        self.motor1.start(dutyCicle)
        self.motor2.start(dutyCicle)
        self.motor3.start(dutyCicle)

        self.A1 = 0
        self.B1 = 0
        self.C1 = 0
        self.A2 = 1
        self.B2 = 1
        self.C2 = 1

        print "OK! -- Wheels set up!"
        return

    def __del__(self):

        self.resetPinInput()
        self.cleanupGPIOPins()
        print "Cleaning up wheel actuator"

    @staticmethod
    def transform(x, y, w):
        initial = [[y], [x], [w]]
        transform = [[0.333, -0.577, 0.333], [-0.667, 0, 0.333], [0.333, 0.577, 0.333]]
        forces = np.matmul(transform, initial)
        return forces

    def Eastmove2point(self, x, y, max_speed):
        controls = self.transform(x, y, 0)
        MAX = max(abs(controls))[0]
        A1new = abs(controls[0])
        B1new = abs(controls[1])
        C1new = abs(controls[2])
        A2new = np.sign(controls[0])
        B2new = np.sign(controls[1])
        C2new = np.sign(controls[2])
        if (A1new != self.A1):
            ANEW = (A1new / MAX) * max_speed  # scaler: usually 100 for fast, 60 for slow
            self.motor1.ChangeDutyCycle(ANEW)  # changes wheel 1 duty cycle (speed)
            self.A1 = A1new  # updates compare value with current value
        if (B1new != self.B1):
            BNEW = (B1new / MAX) * max_speed
            self.motor2.ChangeDutyCycle(BNEW)
            self.B1 = B1new
        if (C1new != self.C1):
            CNEW = (C1new / MAX) * max_speed
            self.motor3.ChangeDutyCycle(CNEW)
            self.C1 = C1new
        if (A2new != self.A2):
            # change pin output to high or low; 1 is low, -1 is high
            if (A2new < 0):
                GPIO.output(26, 1)
            else:
                GPIO.output(26, 0)
            self.A2 = A2new
        if (B2new != self.B2):
            if (B2new < 0):
                GPIO.output(27, 1)
            else:
                GPIO.output(27, 0)
            self.B2 = B2new
        if (C2new != self.C2):
            if (C2new < 0):
                GPIO.output(21, 1)
            else:
                GPIO.output(21, 0)
            self.C2 = C2new

    def linear(self, speed,leg_time):
        self.Eastmove2point(1, 0, speed)
        time.sleep(leg_time)

        # should be run every time a behavior is finished
        self.resetPinInput()

    def serious(self, speed, leg_time):
        # set of points for one serious motion
        points = np.array([[1, 0], [0, 1], [1, 0], [0, -1]])
        for j in range(2):  # repeat 2 times
            for i in range(points.shape[0]):
                self.Eastmove2point(points[i, 0], points[i, 1], speed)
                time.sleep(leg_time)

        # should be run every time a behavior is finished
        self.resetPinInput()

    def spikes(self, speed, leg_time):
        # set of points for one spike motion
        points = np.array([[1, 1], [1, -1]])
        for j in range(4):  # repeat 4 times
            for i in range(points.shape[0]):
                self.Eastmove2point(points[i, 0], points[i, 1], speed)
                time.sleep(leg_time)

        # should be run every time a behavior is finished
        self.resetPinInput()

    def curly(self, speed):
        # create array of sin wave values
        N = 48  # number of samples; 24 for quicker behavior
        # period = (N/2)*0.1 seconds
        ix = np.arange(N)
        amp = 20  # amplitude, arbitrary
        signal = np.sin(2 * np.pi * ix / float(N / 2)) * amp  # y values for 2 sine waves
        x_dist = amp / (N / 8)  # constant x value
        # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

        past_signal = 0
        for i in range(N):
            self.Eastmove2point(x_dist, signal[i] - past_signal, speed)
            time.sleep(0.1)
            past_signal = signal[i]

        # should be run every time a behavior is finished
        self.resetPinInput()

    def loops(self, speed):
        # create array of circle values
        N = 24  # number of samples; 16 for quicker behavior
        # period = N*0.1 seconds
        ix = np.arange(N)
        rad = 20  # radius, arbitrary
        xSignal = np.cos(2 * np.pi / N * ix) * rad  # x values for circle
        ySignal = np.sin(2 * np.pi / N * ix) * rad  # y values for circle
        x_dist = 4  # constant x value for forward motion
        # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

        past_signal_x = 20
        past_signal_y = 0
        for j in range(3):  # repeat 3 times
            for i in range(N):
                self.Eastmove2point(xSignal[i] - past_signal_x + x_dist, ySignal[i] - past_signal_y, speed)
                time.sleep(0.1)
                past_signal_x = xSignal[i]
                past_signal_y = ySignal[i]

        # should be run every time a behavior is finished
        self.resetPinInput()

    def circle(self, speed):
        # create array of circle values
        N = 24  # number of samples; 16 for quicker behavior
        # period = N*0.1 seconds
        ix = np.arange(N)
        rad = 20  # radius, arbitrary
        xSignal = np.cos(2 * np.pi / N * ix) * rad  # x values for circle
        ySignal = np.sin(2 * np.pi / N * ix) * rad  # y values for circle
        # alternatively: create signal array with 1024 elements and sample from it according to inputs period and speed

        past_signal_x = 0
        past_signal_y = 0
        for j in range(2):  # repeat 2 times
            for i in range(N):
                self.Eastmove2point(xSignal[i] - past_signal_x, ySignal[i] - past_signal_y, speed)
                time.sleep(0.1)
                past_signal_x = xSignal[i]
                past_signal_y = ySignal[i]

        # should be run every time a behavior is finished
        self.resetPinInput()

    def performMovement(self, movementType):

        if movementType == Shapes.SPIKES:
            self.spikes(90, 0.5)
        elif movementType == Shapes.RECT:
            self.serious(90, 0.5)
        elif movementType == Shapes.LOOPS:
            self.loops(90)
        elif movementType == Shapes.CURVED:
            self.curly(90)

    def moveTo(self, waypoint, speed):

        self.Eastmove2point(waypoint[0], waypoint[1], speed)

    def resetPinInput(self):

        self.A1 = 0
        self.B1 = 0
        self.C1 = 0
        self.A2 = 1
        self.B2 = 1
        self.C2 = 1

        self.motor1.ChangeDutyCycle(0)
        self.motor2.ChangeDutyCycle(0)
        self.motor3.ChangeDutyCycle(0)

    def cleanupGPIOPins(self):

        try:
            GPIO.output(26, 0)
            GPIO.output(27, 0)
            GPIO.output(21, 0)
            self.motor1.stop()
            self.motor2.stop()
            self.motor3.stop()

        except Exception:
            GPIO.output(26, 0)
            GPIO.output(27, 0)
            GPIO.output(21, 0)
            self.motor1.stop()
            self.motor2.stop()
            self.motor3.stop()
            print("ERROR: There was a problem cleaning up the wheel actuator")

