# inspired in tstenner's @ github

import evdev
import evdev.ecodes as ev


class OpticalSensor:


    def __init__(self):
        self.opticalSensor = None

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
                    #print "read x " + str(inputDictionary["xCoordinate"])
                elif event.code == 1:
                    #inputDictionary["yCoordinate"] = event.value
                    #print "read y " + str(inputDictionary["yCoordinate"])
                    resultList.append(("yCoordinate", event.value))
                elif event.code == 272:
                    # TODO --- Should not work like this in the future"
                    if event.value == 1:
                        resultList.append(("leftButton", 1))
                    else:
                        resultList.append(("leftButton", 0))

            yield resultList
        except IOError:
            #print('Looks like the device was idle since the last read')
            yield


    # just in case other prints are necessary
    def printButtonEvent(self, event):
        states = ['released', 'pressed']
        print('You %s %s at %f.' % (states[event.value], ev.keys[event.code], event.timestamp()))
        yield
