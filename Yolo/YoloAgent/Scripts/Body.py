import numpy
from Libs.Constants import *
from colour import Color
from evdev import InputDevice
from select import select
import collections
import Scripts.Sensors.OpticalSensor
import Scripts.Sensors.TouchSensor
import Scripts.Actuators.StripLEDActuator
import Scripts.Actuators.JewelLEDActuator
from Scripts.Actuators.HeadActuator import HeadActuator
from Scripts.Actuators.WheelActuator import WheelActuator
from Sensors import *
from asyncore import loop
import RPi.GPIO as GPIO

class Body:
    """docstring for Body"""

    def __init__(self):

        self.applicationMode = ApplicationMode.AUTONOMOUS

        # setting the GPIO mode that the board should
        GPIO.setmode(GPIO.BCM)

        # Sensor devices and corresponding demo or auxiliary values
        self.batteryLevel = Battery.OK
        self.accelerationState = Acceleration.SLOW
        self.touchState = Touch.NOT_TOUCHING
        self.touchSensor = Scripts.Sensors.TouchSensor.TouchSensor()

        self.opticalSensorDevice = Scripts.Sensors.OpticalSensor.OpticalSensor()  # InputDevice('/dev/input/event0')
        self.opticalState = Optical.NOT_RECEIVING
        self.opticalShape = collections.deque(maxlen=200)
        self.newOpticalInfo = None
        self.opticalSensorPosition = [0, 0]

        # Actuator devices and corresponding demo or auxiliary values
        self.LEDJewel = Scripts.Actuators.JewelLEDActuator.JewelLEDActuator()
        self.LEDStrip = Scripts.Actuators.StripLEDActuator.StripLEDActuator()
        self._color = Color(rgb=(0.0, 0.0, 0.0))
        self._colorBrightness = ColorBrightnessValues[ColorBrightness.MEDIUM.name]


        # wheel controls
        self.wheelActuator = WheelActuator()

        # head controls
        self.headActuator = HeadActuator()
        # value between 0 (completely retracted) and 100 (fully extended) for the agent's feelers
        self._feelerPositionPercentage = 100
        self._feelerGearRatio = 1.0

        print "Component set up finished!"

        return

    def __del__(self):

        self.touchSensor = None
        self.wheelActuator = None
        self.opticalSensorDevice = None
        self.LEDJewel = None
        self.LEDStrip = None

        self.cleanupGPIOPins()

        print "Component cleanup successful!"

    ## GETTERS

    def getSensorData(self):

        sensorData = []

        sensorData.append(self.getTouchSensorData())
        sensorData.append(self.getOpticalSensorData())
        sensorData.append(self.getAccelerationSensorData())

        #print(sensorData)

        return sensorData

    def getOpticalSensorData(self):

        if self.applicationMode is ApplicationMode.DEMO or not self.opticalSensorDevice.isOpticalSensorConnected():

            if self.opticalState is Optical.RECEIVING:
                self.opticalShape.append(self.newOpticalInfo)
                return (Sensor.OPTICAL, (Optical.RECEIVING, list(self.opticalShape)))
            elif self.opticalState is Optical.FINISHED:
                shapeToReturn = list(self.opticalShape)
                self.opticalState = Optical.NOT_RECEIVING
                return (Sensor.OPTICAL, (Optical.FINISHED, shapeToReturn))
            elif self.opticalState is Optical.NOT_RECEIVING:
                return (Sensor.OPTICAL, (Optical.NOT_RECEIVING, list(self.opticalShape)))
            else:
                print ("Error: This option shouldn't be selected!")
        else:

            resultList = []
            for eventList in self.opticalSensorDevice.getEvents():
                if eventList is not None:
                    resultList = eventList

            for event in resultList:
                if event[0] == "xCoordinate":
                    self.opticalSensorPosition[0] = self.opticalSensorPosition[0] + int(event[1])
                elif event[0] == "yCoordinate":
                    self.opticalSensorPosition[1] = self.opticalSensorPosition[1] + int(event[1])
                # Note: to be able to test the pattern recognition using only mouse events as triggers - just uncomment
                #elif event[0] == "leftButton":
                    #if event[1] == 1:
                    #    self.touchState = Touch.TOUCHING
                    #else:
                    #    self.touchState = Touch.NOT_TOUCHING

            if self.opticalState is Optical.NOT_RECEIVING and self.touchState is Touch.TOUCHING:
                self.opticalShape.clear()
                self.opticalState = Optical.RECEIVING
                self.opticalShape.append((self.opticalSensorPosition[0], self.opticalSensorPosition[1]))
            elif self.opticalState is Optical.RECEIVING and self.touchState is Touch.TOUCHING:
                newPosition = (self.opticalSensorPosition[0], self.opticalSensorPosition[1])

                #Note: to eliminate possible reads that return the same position
                if self.opticalShape[-1] != newPosition:
                    self.opticalShape.append(newPosition)
            elif self.opticalState is Optical.RECEIVING and self.touchState is Touch.NOT_TOUCHING:
                self.opticalShape.append((self.opticalSensorPosition[0], self.opticalSensorPosition[1]))

                #Note: to avoids really small touches on the robot to be read as shapes
                if len(self.opticalShape) > 30:
                    self.opticalState = Optical.FINISHED
                    #print self.opticalShape
                else:
                    self.opticalState = Optical.NOT_RECEIVING
                    self.opticalShape.clear()
                    self.opticalSensorPosition = [0, 0]
            elif self.opticalState is Optical.FINISHED:
                self.opticalState = Optical.NOT_RECEIVING
                self.opticalShape.clear()
                self.opticalSensorPosition = [0, 0]

            return (Sensor.OPTICAL, (self.opticalState, self.opticalShape))

    def getAccelerationSensorData(self):

        if self.applicationMode == ApplicationMode.DEMO:
            return (Sensor.ACCEL, self.accelerationState)
        else:
            # TODO read from actual sensor
            return (Sensor.ACCEL, Acceleration.FAST)

    def getTouchSensorData(self):

        if self.applicationMode == ApplicationMode.DEMO:
            return (Sensor.TOUCH, self.touchState)
        else:
            self.touchState = self.touchSensor.getTouchInput()
            return (Sensor.TOUCH, self.touchState)

    def getColor(self):
        return self._color

    def getBrightness(self):
        return self._colorBrightness

    def getFeelerPosition(self):
        return self._feelerPositionPercentage

    # NOTE: pathDistance is a value between 0-100 and time a value in seconds
    def getFeelerSpeed(self, pathPercentageDistance, time):

        # NOTE: 28/11/17 -- 7.0 stops, 8.0 for 0.85 seconds will go totally down and  6.0 for 0.85 will go totally up

        if pathPercentageDistance == 0:
            return 0

        # NOTE - the track's size is 10 cm
        realSizeOfTrack = 10

        # converting between a percentage value (which could be negative if going down to real distance in track
        trackDistance = Body.translate(numpy.abs(pathPercentageDistance), 0, 100, 0, realSizeOfTrack)

        speed = time / (trackDistance * self._feelerGearRatio)

        # TODO - there has to be a conversion between the distance covered per second by the motor so that I can convert it to a range between 0-100 for instance
        speed = 8.0

        return speed

    # NOTE: pathPercentageDistance and speedPercentage are a values between 0-100
    def getFeelerMovementTime(self, pathPercentageDistance, speedPercentage):

        if pathPercentageDistance == 0:
            return 0

        # NOTE - the track's size is 10 cm
        realSizeOfTrack = 10

        # converting between a percentage value (which could be negative if going down to real distance in track
        trackDistance = Body.translate(numpy.abs(pathPercentageDistance), 0, 100, 0, realSizeOfTrack)
        print("Path, converting percentage: " + str(pathPercentageDistance) + ", to real track: " + str(trackDistance))

        # TODO- find out the real speed and change last range accordingly, assuming counter clockwise goes up and going is positive distance
        if pathPercentageDistance >= 0:
            speed = Body.translate(speedPercentage, 0, 100, 0,
                                   2.5)  # TODO- these are the voltages see how to integrate them - 1500, 2300)
        else:
            speed = Body.translate(speedPercentage, -100, 0, -2.5,
                                   0)  # TODO- these are the voltages see how to integrate them - 700, 1500)

        time = speed / (trackDistance * self._feelerGearRatio)

        return time

    @staticmethod
    def translate(value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    ## SETTERS

    def setColor(self, newColor):
        self._color = newColor
        #Note: I separate the color into its channel to avoid confusing between the Color module I was using and the one defined by NeoPixel
        r = self.translate(newColor.red, 0, 1, 0, 255)
        g = self.translate(newColor.green, 0, 1, 0, 255)
        b = self.translate(newColor.blue, 0, 1, 0, 255)

        # cleaning up any imprecision
        r = numpy.clip(r, 0, 255)
        g = numpy.clip(g, 0, 255)
        b = numpy.clip(b, 0, 255)

        #Note: the LEDs will clip any value to integer
        self.LEDJewel.setColor(r, g, b)
        self.LEDStrip.setColor(r, g, b)
        #print ("Setting LEDs to " + str(newColor))

        return

    def setBrightness(self, newBrightness):
        self._colorBrightness = newBrightness

        self.LEDJewel.setBrightness(newBrightness)
        self.LEDStrip.setBrightness(newBrightness)

    # NOTE: this function is a percentage
    def setFeelerPosition(self, newFeelerPositionPercentage):
        self._feelerPositionPercentage = newFeelerPositionPercentage
        print ("Setting feelers to " + str(newFeelerPositionPercentage))

        return

    def setFeelerMovement(self, speedPercentage):

        return
        # Note: motor stop with 1500 voltage
        if speedPercentage == 0:
            speedToBeSet = 7.5
        # TODO- find out the real speed and change last range accordingly, assuming counter clockwise goes up and going is positive distance
        elif 0 > speedPercentage > 100:
            speedToBeSet = Body.translate(speedPercentage, 0, 100, 7.0, 2.0)
        elif -100 < speedPercentage < 0:
            speedToBeSet = Body.translate(speedPercentage, -100, 0, 12.0, 7.0)
        else:
            raise Exception("Error: speed for the is out of bounds")

        self.headActuator.moveTo(speedToBeSet)

        #print ("Setting feelers to speed " + str(speedToBeSet))

        return

    def setWheelMovement(self, movementType, waypoint, speed):

        self.wheelActuator.moveTo(waypoint, speed)

        #print ("Setting movement to: " + str(movementType))

        return

    def resetWheelSetup(self):
        self.wheelActuator.resetPinInput()

    ## AUXILIARY FUNCTIONS

    def toggleApplicationMode(self):

        if self.applicationMode == ApplicationMode.AUTONOMOUS:
            self.applicationMode = ApplicationMode.DEMO
        elif self.applicationMode == ApplicationMode.DEMO:
            self.applicationMode = ApplicationMode.AUTONOMOUS

        print ("Switched application mode to " + self.applicationMode.name)


    def cleanupGPIOPins(self):

        try:
            GPIO.cleanup()

        except Exception:
            print("ERROR: There was a problem cleaning up GPIO")
