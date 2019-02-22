from asyncore import loop
import RPi.GPIO as GPIO
from colour import Color
from Libs.Constants import *
from Scripts.Sensors.OpticalSensor import OpticalSensor
from Scripts.Sensors.TouchSensor import TouchSensor
from Scripts.Actuators.LEDActuator import LEDActuator
from Scripts.Actuators.WheelActuator import WheelActuator

class Body:
    def __init__(self, stimulusColor):
        # setting the GPIO mode that the board should
        GPIO.setmode(GPIO.BCM)

        self.stimulusColor = stimulusColor;
        self.touchSensor = TouchSensor()
        self.opticalSensor = OpticalSensor()
        self.LEDActuator = LEDActuator()
        self.wheelActuator = WheelActuator()
        self.color = Color(rgb=(0.0, 0.0, 0.0))
        self.colorBrightness = ColorBrightnessValues[ColorBrightness.MEDIUM.name]
        print "Body set up finished!"
        return

    def __del__(self):
        self.touchSensor = None
        self.wheelActuator = None
        self.opticalSensor = None
        self.LED = None
        self.cleanupGPIOPins()
        print "Body cleanup successful!"

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
   
    def setColor(self, newColor):
        self.color = newColor
        self.LEDActuator.setColor(newColor.red, newColor.green, newColor.blue)  #Note: the LEDs will clip any value to integer

    def setBrightness(self, newBrightness):
        self.colorBrightness = newBrightness
        self.LEDActuator.setBrightness(newBrightness)

    def setWheelMovement(self, waypoint, speed):
        self.wheelActuator.moveTo(waypoint, speed)

    def resetWheelSetup(self):
        self.wheelActuator.resetPinInput()

    def cleanupGPIOPins(self):
        try:
            GPIO.cleanup()
        except Exception:
            print("ERROR: There was a problem cleaning up the Body's GPIO")