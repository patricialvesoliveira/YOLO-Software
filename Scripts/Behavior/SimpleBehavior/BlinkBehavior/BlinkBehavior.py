import time
import numpy
from colour import Color
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.SimpleBehavior import SimpleBehavior


class BlinkBehavior(SimpleBehavior):
    def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting, startDelay = 0.0, animationPause = 0.0):
        SimpleBehavior.__init__(self, bodyRef, repetitions, duration, keepBehaviorSetting, startDelay)
        self.bodyRef = bodyRef
        self.behaviorType = BehaviorType.BLINK
        self.bodyColorAtStart = bodyRef.getColor()
        self.bodyBrightnessAtStart = bodyRef.getBrightness()
        self.blinkColorList = blinkColorList
        self.activeBlinkColor = blinkColorList[0]
        self.brightness = brightness
        self.activeBlinkBrightness = ColorBrightnessValues[brightness.name]
        self.animationEndPause = animationPause
        self.defaultColor = defaultColor
        self.duration = duration

    def behaviorActions(self):
        # when the animation is over we pause before changing color
        if self.checkForBehaviorEnd():
            if self.maxBehaviorRepetitions!=0:
                if self.currentBehaviorRepetition == self.maxBehaviorRepetitions:
                    self.finishBehavior()
                    print("Behavior ended")
                    return

                if self.currentBehaviorRepetition > self.maxBehaviorRepetitions:
                    return

                self.currentBehaviorRepetition += 1
            self.startTime = time.time()
            self.activeBlinkColor = self.blinkColorList[(self.currentBehaviorRepetition-1) % len(self.blinkColorList)]
        return

    def finishBehavior(self):
        SimpleBehavior.finishBehavior(self)
        print "keepBehaviorSetting: "+str(self.keepBehaviorSetting)
        if self.keepBehaviorSetting:
            self.bodyRef.setColor(self.activeBlinkColor)
            self.bodyRef.setBrightness(self.activeBlinkBrightness)
        else:
            self.bodyRef.setColor(self.defaultColor)
        return

    

    def animateLerp(self, percentage):
        self.bodyRef.setColor(self.lerpColor(percentage, self.bodyColorAtStart, self.activeBlinkColor))
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