import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behaviors.SimpleBehaviors.Behavior import Behavior


class BlinkBehavior(Behavior):
    def __init__(self):
        Behavior.__init__(self)

        self.behaviorType = Behaviors.BLINK  # Configuration.Behaviors
        self._animationEndPause = 0
        self.blinkTransition = Transitions.LINEAR
        self.color = Color("black")
        self.colorBrightness = ColorBrightness.MEDIUM
        self.activeBlinkColor = Color("white")
        self.blinkColorList = [Color("white")]
        self.blinkBrightness = ColorBrightness.MEDIUM
        self.defaultColor = None

        return

    # Body body, int repetitions, float duration
    def prepareBehavior(self, body, blinkColorList, brightness, transition, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
        Behavior.prepareBehavior(self, body, transition, repetitions, duration, keepBehaviorSetting, startDelay)
        self.color = body.getColor()
        self.colorBrightness = body.getBrightness()
        self.blinkColorList = blinkColorList
        self.activeBlinkColor = self.blinkColorList[0]
        self.blinkBrightness = ColorBrightnessValues[brightness.name]
        self.blinkTransition = transition
        self._animationEndPause = animationPause
        self.defaultColor = defaultColor

        return

    # Body body
    def applyBehavior(self, body):

        # Note: allows for a delayed start
        if self.shouldStartBeDelayed():
            return

        #print ("Applying blink ")

        if self.blinkTransition == Transitions.LINEAR:
            lerp = (time.time() - self._startTime) / self._animationIntervalTime
            body.setColor(self.lerpColor(lerp, self.color, self.activeBlinkColor))
            body.setBrightness(self.blinkBrightness * lerp + self.colorBrightness * (1 - lerp))
            print("Applying blink: passed " + str((time.time() - self._startTime)) + " of " + str(self._animationIntervalTime) + ". Lerp: " + str(lerp))

        elif self.blinkTransition == Transitions.INSTANT:
            body.setColor(self.activeBlinkColor)
            self.isOver = True
            return

        elif self.blinkTransition == Transitions.EASEIN:
            timeElapsed = time.time() - self._startTime
            lerp = tween.easeInSine(numpy.clip(timeElapsed / self._animationIntervalTime, 0, 1))
            body.setColor(self.lerpColor(lerp, self.color, self.activeBlinkColor))
            body.setBrightness(self.blinkBrightness * lerp + self.colorBrightness * (1 - lerp))

        elif self.blinkTransition == Transitions.EASEOUT:
            timeElapsed = time.time() - self._startTime
            lerp = tween.easeOutSine(numpy.clip(timeElapsed / self._animationIntervalTime, 0, 1))
            body.setColor(self.lerpColor(lerp, self.color, self.activeBlinkColor))
            body.setBrightness(self.blinkBrightness * lerp + self.colorBrightness * (1 - lerp))

        elif self.blinkTransition == Transitions.EASEINOUT:
            totalTime = self._animationIntervalTime / 2

            if time.time() - self._startTime <= totalTime:
                timeElapsed = time.time() - self._startTime
                lerp = tween.easeInSine(numpy.clip(timeElapsed / totalTime, 0, 1))
                body.setColor(self.lerpColor(lerp, self.color, self.activeBlinkColor))
                body.setBrightness(self.blinkBrightness * lerp + self.colorBrightness * (1 - lerp))

                # print("easing in: " + lerp)
            # when the  animation is over  we can pause before changing color
            elif time.time() - self._startTime >= totalTime + self._animationEndPause:
                # Note: since behavior can be interrupted arbitrarily the color the body currently has can be unexpected
                # and easingIn n Out will end up leaving it the same
                if self.defaultColor is not None:
                    self.color = self.defaultColor

                timeElapsed = (time.time() - self._startTime - self._animationEndPause) - totalTime
                lerp = 1 - tween.easeOutSine(numpy.clip(timeElapsed / totalTime, 0, 1))
                body.setColor(self.lerpColor(lerp, self.color, self.activeBlinkColor))
                body.setBrightness(self.blinkBrightness * lerp + self.colorBrightness * (1 - lerp))

                # print("easing out: " + (1 - lerp))

        # when the animation is over we pause before changing color
        if time.time() - self._startTime > self._animationIntervalTime + self._animationEndPause:
            if self._currentBehaviorRepetition == self._maxBehaviorRepetitions:

                self.finalizeEffects(body)
                print("Behavior ended")
                return

            self._currentBehaviorRepetition += 1
            self.activeBlinkColor = self.blinkColorList[(self._currentBehaviorRepetition-1) % len(self.blinkColorList)]
            self._startTime = time.time()

        return

    # Body body
    def finalizeEffects(self, body):
        if self.keepBehaviorSetting == True:
            body.setColor(self.activeBlinkColor)
            print("setting the animation end color")
        else:
            body.setColor(self.color)

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
