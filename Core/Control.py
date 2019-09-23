from asyncore import loop
import RPi.GPIO as GPIO
from colour import Color
from Core.Enumerations import *
from Core.Sensors.OpticalSensor import OpticalSensor
from Core.Sensors.TouchSensor import TouchSensor
from Core.Actuators.LEDActuator import LEDActuator
from Core.Actuators.WheelActuator import WheelActuator

class Control:
    def __init__(self):
        # remove GPIO warnings
        GPIO.setwarnings(False)
        # setting the GPIO mode that the board should
        GPIO.setmode(GPIO.BCM)
        self.touchSensor = TouchSensor()
        self.opticalSensor = OpticalSensor()
        self.LEDActuator = LEDActuator()
        self.wheelActuator = WheelActuator()
        self.color = Color(rgb=(0.0, 0.0, 0.0))

        self.colorBrightness = ColorBrightness.MEDIUM
        print "Control set up finished!"

    def __del__(self):
        self.touchSensor = None
        self.opticalSensor = None
        self.LEDActuator = None
        self.wheelActuator = None
        self.cleanupGPIOPins()
        print "Control cleanup successful!"

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
            print("ERROR: There was a problem cleaning up the Control's GPIO")