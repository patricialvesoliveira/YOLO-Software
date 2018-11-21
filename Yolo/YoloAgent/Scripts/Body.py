from Libs.Constants import *
from colour import Color

from Scripts.Sensors.OpticalSensor import OpticalSensor
from Scripts.Sensors.TouchSensor import TouchSensor

from Scripts.Actuators.LEDActuator import LEDActuator
from Scripts.Actuators.WheelActuator import WheelActuator

from asyncore import loop
import RPi.GPIO as GPIO

import traceback

class Body:
    """docstring for Body"""

    def __init__(self, stimulusColor):

        # setting the GPIO mode that the board should
        GPIO.setmode(GPIO.BCM)

        self.stimulusColor = stimulusColor;

        # Sensor devices and corresponding demo or auxiliary values
        self.touchSensor = TouchSensor()
        self.opticalSensor = OpticalSensor()

        # Actuator devices and corresponding demo or auxiliary values
        self.LEDActuator = LEDActuator()
        self.wheelActuator = WheelActuator()
        
        # Body stuff
        self.color = Color(rgb=(0.0, 0.0, 0.0))
        self.colorBrightness = ColorBrightnessValues[ColorBrightness.MEDIUM.name]

        print "Component set up finished!"
        return

    def __del__(self):

        self.touchSensor = None
        self.wheelActuator = None
        self.opticalSensor = None
        self.LED = None

        self.cleanupGPIOPins()
        print "Component cleanup successful!"

    def update(self):
        self.updateTouchSensorData()
        self.updateOpticalSensorData()

    def updateOpticalSensorData(self):
        if self.touchSensor.getState() == TouchState.TOUCHING and self.opticalSensor.getState() == OpticalState.NOT_RECEIVING:
            self.opticalSensor.setState(OpticalState.RECEIVING);

        if self.touchSensor.getState() == TouchState.NOT_TOUCHING and self.opticalSensor.getState() == OpticalState.RECEIVING:
            self.opticalSensor.setState(OpticalState.NOT_RECEIVING);
        
        self.opticalSensor.update()

    def updateTouchSensorData(self):
        self.touchSensor.update()


    def getTouchSensor(self):
        return self.touchSensor

    def getOpticalSensor(self):
        return self.opticalSensor


    def getStimulusColor(self):
        return self.stimulusColor
    def getColor(self):
        return self.color

    def getBrightness(self):
        return self.colorBrightness
   
    # SETTERS
    def setColor(self, newColor):
        self.color = newColor
        # print "setColor:" + str(newColor)
        # traceback.print_stack()
        self.LEDActuator.setColor(newColor.red, newColor.green, newColor.blue)  #Note: the LEDs will clip any value to integer

    def setBrightness(self, newBrightness):
        self.colorBrightness = newBrightness
        self.LEDActuator.setBrightness(newBrightness)

    def setWheelMovement(self, waypoint, speed):
        self.wheelActuator.moveTo(waypoint, speed)
        # print "setWheelMovement"

    def resetWheelSetup(self):
        self.wheelActuator.resetPinInput()
        # print "resetWheelMovement"


    def cleanupGPIOPins(self):
        try:
            GPIO.cleanup()

        except Exception:
            print("ERROR: There was a problem cleaning up GPIO")


 
