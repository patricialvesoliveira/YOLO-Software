import time
import numpy
from colour import Color
from Core.Enumerations import *
from Core.Behavior.SimpleBehavior.SimpleBehavior import SimpleBehavior


class BlinkBehavior(SimpleBehavior, object):
    def __init__(self, bodyRef, blinkColor, brightness, maxBehaviorRepetitions, duration, defaultColor):
        super(BlinkBehavior, self).__init__(bodyRef, maxBehaviorRepetitions, duration)
        self.bodyRef = bodyRef
        self.bodyColorAtStart = bodyRef.getColor()
        self.bodyBrightnessAtStart = bodyRef.getBrightness()
        self.blinkColor = blinkColor
        self.brightness = brightness
        self.defaultColor = defaultColor
        # self.duration = duration
        

    def behaviorActions(self):
        #to be overriden
        super(BlinkBehavior, self).behaviorActions()
        

    def finishBehavior(self):
        super(BlinkBehavior, self).finishBehavior()
        self.bodyRef.setColor(self.defaultColor)

    def checkForBehaviorEnd(self): 
        return time.time() - self.startTime > self.duration  
              
    def lerpColor(self, percentage, currentColor, newColor):
        rLerp = newColor.red * percentage + currentColor.red * (1 - percentage)
        gLerp = newColor.green * percentage + currentColor.green * (1 - percentage)
        bLerp = newColor.blue * percentage + currentColor.blue * (1 - percentage)

        #cleaning up any imprecision
        rLerp = numpy.clip(rLerp, 0, 1)
        gLerp = numpy.clip(gLerp, 0, 1)
        bLerp = numpy.clip(bLerp, 0, 1)

        lerpColor = Color(rgb=(rLerp, gLerp, bLerp))
        return lerpColor
