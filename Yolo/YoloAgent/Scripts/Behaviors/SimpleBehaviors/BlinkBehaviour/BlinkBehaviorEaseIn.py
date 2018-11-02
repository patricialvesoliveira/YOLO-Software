import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import BlinkBehavior


class BlinkBehaviorEaseIn(BlinkBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, body, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
        BlinkBehavior.__init__(self, body, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting, startDelay, animationPause)
    
    # Body body
    def applyBehavior(self, body):
        BlinkBehavior.applyBehavior(body)
        timeElapsed = time.time() - self._startTime
        percentage = tween.easeInSine(numpy.clip(timeElapsed / self._animationIntervalTime, 0, 1))
        self.animateLerp(percentage)
