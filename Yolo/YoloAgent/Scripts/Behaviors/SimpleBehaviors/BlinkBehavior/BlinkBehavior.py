import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behaviors.SimpleBehaviors.Behavior import Behavior


class BlinkBehavior(Behavior):
    def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
        Behavior.__init__(self, bodyRef, repetitions, duration, keepBehaviorSetting, startDelay)

        self.bodyRef = bodyRef

        self.behaviorType = Behaviors.BLINK  # Configuration.Behaviors

        self.color = bodyRef.getColor()
        self.colorBrightness = bodyRef.getBrightness()

        self.blinkColorList = blinkColorList
        self.activeBlinkColor = self.blinkColorList[0]
        self.blinkBrightness = ColorBrightnessValues[brightness.name]
        self._animationEndPause = animationPause
        self.defaultColor = defaultColor

    # Body body
    def applyBehavior(self):
        # Note: allows for a delayed start
        if self.shouldStartBeDelayed():
            return

        # when the animation is over we pause before changing color
        if time.time() - self._startTime > self._animationIntervalTime + self._animationEndPause:
            if self._currentBehaviorRepetition == self._maxBehaviorRepetitions:
                self.finalizeEffects()
                print("Behavior ended")
                return

            self._currentBehaviorRepetition += 1
            self.activeBlinkColor = self.blinkColorList[(self._currentBehaviorRepetition-1) % len(self.blinkColorList)]
            self._startTime = time.time()


    def finalizeEffects(self):
        if self.keepBehaviorSetting == True:
            self.bodyRef.setColor(self.activeBlinkColor)
            print("setting the animation end color")
        else:
            self.bodyRef.setColor(self.color)

        self.isOver = True
        return

    def lerpColor(self, lerp, currentColor, newColor):

        rLerp = newColor.red * lerp + currentColor.red * (1 - lerp)
        gLerp = newColor.green * lerp + currentColor.green * (1 - lerp)
        bLerp = newColor.blue * lerp + currentColor.blue * (1 - lerp)

        #cleaning up any imprecision
        rLerp = numpy.clip(rLerp, 0, 1)
        gLerp = numpy.clip(gLerp, 0, 1)
        bLerp = numpy.clip(bLerp, 0, 1)

        #print("Color - Lerp: " + str(lerp) + ", rgb: " + str(rLerp) + "," + str(gLerp) + "," + str(bLerp))
        lerpColor = Color(rgb=(rLerp, gLerp, bLerp))

        #print("color: " + str(currentColor) + ", blink: " + str(newColor) + ", finalColor: " + str(lerpColor.rgb))

        return lerpColor

    def animateLerp(self, percentage):
        print self.bodyRef.getColor()
        breakpoint()
        self.bodyRef.setColor(self.lerpColor(percentage, self.color, self.activeBlinkColor))
        self.bodyRef.setBrightness(self.blinkBrightness * percentage + self.colorBrightness * (1 - percentage))
        print("Applying blink: passed " + str((time.time() - self._startTime)) + " of " + str(self._animationIntervalTime) + ". Lerp: " + str(lerp))
