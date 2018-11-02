from Libs.Constants import *
from colour import Color

from Scripts.Sensors.OpticalSensor import OpticalSensor
from Scripts.Sensors.TouchSensor import TouchSensor

from Scripts.Actuators.LEDActuator import LEDActuator
from Scripts.Actuators.WheelActuator import WheelActuator

from asyncore import loop
import RPi.GPIO as GPIO

class Body:
    """docstring for Body"""

    def __init__(self):
        self.applicationMode = ApplicationMode.AUTONOMOUS

        # setting the GPIO mode that the board should
        GPIO.setmode(GPIO.BCM)

        # Sensor devices and corresponding demo or auxiliary values
        self.touchSensor = TouchSensor()
        self.opticalSensor = OpticalSensor()

        # Actuator devices and corresponding demo or auxiliary values
        # self.LEDActuator = LEDActuator()
        # self.wheelActuator = WheelActuator()
        
        # Body stuff
        self._color = Color(rgb=(0.0, 0.0, 0.0))
        self._colorBrightness = ColorBrightnessValues[ColorBrightness.MEDIUM.name]

        print "Component set up finished!"
        return

    def __del__(self):

        self.touchSensor = None
        self.wheelActuator = None
        self.opticalSensor = None
        self.LED = None

        self.cleanupGPIOPins()
        print "Component cleanup successful!"

    # GETTERS
    def getSensorData(self):
        sensorData = []
        sensorData.append(self.getTouchSensorData())
        sensorData.append(self.getOpticalSensorData())
        return sensorData

    def getOpticalSensorData(self):
        if self.touchSensor.touchState is Touch.TOUCHING and self.opticalSensor.opticalState is Optical.NOT_RECEIVING:
            self.opticalSensor.changeState(Optical.RECEIVING);

        if self.touchSensor.touchState is Touch.NOT_TOUCHING and self.opticalSensor.opticalState is Optical.RECEIVING:
            self.opticalSensor.changeState(Optical.NOT_RECEIVING);

        return self.opticalSensor.recordOpticalInput()

    def getTouchSensorData(self):
        return self.touchSensor.recordTouchInput()

    def getColor(self):
        return self._color

    def getBrightness(self):
        return self._colorBrightness
   
    # SETTERS
    def setColor(self, newColor):
        self._color = newColor
        # self.LEDActuator.setColor(newColor.red, newColor.green, newColor.blue)  #Note: the LEDs will clip any value to integer

    def setBrightness(self, newBrightness):
        self._colorBrightness = newBrightness
        # self.LEDActuator.setBrightness(newBrightness)

    def setWheelMovement(self, waypoint, speed):
        # self.wheelActuator.moveTo(waypoint, speed)
        print "setWheelMovement"

    def resetWheelSetup(self):
        # self.wheelActuator.resetPinInput()
        print "resetWheelMovement"


    def cleanupGPIOPins(self):
        try:
            GPIO.cleanup()

        except Exception:
            print("ERROR: There was a problem cleaning up GPIO")


 
