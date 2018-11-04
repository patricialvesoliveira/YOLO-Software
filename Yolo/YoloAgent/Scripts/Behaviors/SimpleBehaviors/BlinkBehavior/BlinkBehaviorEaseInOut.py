import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior.BlinkBehavior import BlinkBehavior


class BlinkBehaviorEaseInOut(BlinkBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
        BlinkBehavior.__init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, False, startDelay, animationPause)

    # Body body
    def applyBehavior(self):
        BlinkBehavior.applyBehavior(self)
        
        timeElapsed = time.time() - self.startTime
        totalTime = self.animationIntervalTime / 2

        if time.time() - self.startTime <= totalTime:
            percentage = tween.easeInSine(numpy.clip(timeElapsed / totalTime, 0, 1))

        # when the  animation is over  we can pause before changing color
        elif time.time() - self.startTime >= totalTime + self.animationEndPause:
            if self.defaultColor is not None:
                self.color = self.defaultColor
            percentage = 1 - tween.easeOutSine(numpy.clip(timeElapsed / totalTime, 0, 1))

        self.animateLerp(percentage)
