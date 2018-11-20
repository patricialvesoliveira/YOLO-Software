# inspired in tstenner's @ github
import collections
from Libs.Constants import *


import evdev
import evdev.ecodes as ev


class OpticalSensor:

    def __init__(self):
        self.opticalSensor = None

        self.sensorType = SensorType.OPTICAL

        self.state = OpticalState.NOT_RECEIVING
        self.opticalShape = collections.deque(maxlen=200)
        self.newOpticalInfo = None
        self.opticalSensorPosition = [0, 0]

        

        for fn in evdev.list_devices():
            dev = evdev.InputDevice(fn)
            cap = dev.capabilities()

            if ev.EV_KEY in cap:
                if ev.BTN_MOUSE in cap[ev.EV_KEY]:
                    self.opticalSensor = dev
                    print "OK! -- Optical sensor: " + str(self.opticalSensor) + " set up!"
                    return

        if self.opticalSensor is None:
            print "Error: The optical sensor is not connected! Can only run in Demo mode"
            #raise Exception("Error: The optical sensor is not connected!")

    def isOpticalSensorConnected(self):
        return self.opticalSensor is not None

    def getEvents(self):
        self.opticalSensor.grab()
        self.opticalSensor.read()  # discard input buffer
        self.opticalSensor.ungrab()

        try:
            events = list(self.opticalSensor.read())
            resultList = []
            for event in events:
                if event.code == 0:
                    resultList.append(("xCoordinate", event.value))
                elif event.code == 1:
                    resultList.append(("yCoordinate", event.value))
                #Note: to be able to test the pattern recognition using only mouse events as triggers - just uncomment
                #elif event.code == 272:
                #    if event.value == 1:
                #        resultList.append(("leftButton", 1))
                #    else:
                #        resultList.append(("leftButton", 0))

            yield resultList
        except IOError:
            # print('Looks like the device was idle since the last read')
            yield



    def update(self):

        if not self.isOpticalSensorConnected():

            if self.state is OpticalState.RECEIVING:
                self.insertNewPathPosition(self.opticalShape, self.newOpticalInfo)

            elif self.state is OpticalState.NOT_RECEIVING:
                if self.state is OpticalState.RECEIVING:
                    opticalState = OpticalState.FINISHED
                # do nothing
                a = 0;

            elif self.state is OpticalState.FINISHED:
                # self.currentRecorgnizedShape = list(self.opticalShape)
                self.state = OpticalState.NOT_RECEIVING

            else:
                print ("Error: This option shouldn't be selected!")
        else:
            
            resultList = []
            for eventList in self.getEvents():
                if eventList is not None:
                    resultList = eventList

            for event in resultList:
                if event[0] == "xCoordinate":
                    self.opticalSensorPosition[0] = self.opticalSensorPosition[0] + int(event[1])
                elif event[0] == "yCoordinate":
                    self.opticalSensorPosition[1] = self.opticalSensorPosition[1] + int(event[1])
 

            if self.state is OpticalState.RECEIVING:
                newPosition = (self.opticalSensorPosition[0], self.opticalSensorPosition[1])
                self.insertNewPathPosition(self.opticalShape, newPosition)

                 #Note: to avoids really small touches on the robot to be read as shapes
                if len(self.opticalShape) > 30:
                    self.state = OpticalState.FINISHED
                    # print self.opticalShape


            elif self.state is OpticalState.NOT_RECEIVING:

                self.opticalSensorPosition = [0, 0]


            elif self.state is OpticalState.FINISHED:

                self.opticalShape.clear()
                self.opticalSensorPosition = [0, 0]
                self.state = OpticalState.NOT_RECEIVING



    def setState(self,state):
        self.state = state
    def getState(self):
        return self.state

    def getCurrentRecognizedShape(self):
        return self.opticalShape

    def insertNewPathPosition(self,path,newPosition):
        if newPosition == None:
            return
        #Note: to eliminate possible reads that return the same position
        if len(path) == 0:
            path.append(newPosition)
        elif path[-1] != newPosition:
            path.append(newPosition)


    def printButtonEvent(self, event):
        states = ['released', 'pressed']
        print('You %s %s at %f.' % (states[event.value], ev.keys[event.code], event.timestamp()))
        yield
