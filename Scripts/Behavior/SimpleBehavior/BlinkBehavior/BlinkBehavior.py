import time
import numpy
from colour import Color
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.SimpleBehavior import SimpleBehavior


class BlinkBehavior(SimpleBehavior):
    def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
        SimpleBehavior.__init__(self, bodyRef, repetitions, duration)
        self.bodyRef = bodyRef
        self.bodyColorAtStart = bodyRef.getColor()
        self.bodyBrightnessAtStart = bodyRef.getBrightness()
        self.blinkColor = blinkColor
        self.brightness = brightness
        self.activeBlinkBrightness = ColorBrightnessValues[brightness.name]
        self.defaultColor = defaultColor

        self.initBehavior()

    def initBlink(self):
        self.startTime = time.time()

    def initBehavior(self):
        SimpleBehavior.initBehavior(self)
        self.initBlink()
        
    def behaviorActions(self):
        # when the animation is over we pause before changing color
        if self.checkForBehaviorEnd():
            if self.maxBehaviorRepetitions!=0:
                self.currentBehaviorRepetition += 1
                print self.currentBehaviorRepetition
                if self.currentBehaviorRepetition >= self.maxBehaviorRepetitions:
                    self.finishBehavior()
                    return
                self.initBlink()

    def finishBehavior(self):
        SimpleBehavior.finishBehavior(self)
        self.bodyRef.setColor(self.defaultColor)

    

    def animateLerp(self, percentage):
        self.bodyRef.setColor(self.lerpColor(percentage, self.bodyColorAtStart, self.blinkColor))
        self.bodyRef.setBrightness(self.activeBlinkBrightness * percentage + self.bodyBrightnessAtStart * (1 - percentage))

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


    def checkForBehaviorEnd(self): 
        return time.time() - self.startTime > self.duration