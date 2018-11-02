import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import BlinkBehavior


class BlinkBehaviorLinear(BlinkBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, body, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
        BlinkBehavior.__init__(self, body, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting, startDelay, animationPause)

    # Body body
    def applyBehavior(self, body):
        BlinkBehavior.applyBehavior(body)
        percentage = (time.time() - self._startTime) / self._animationIntervalTime
        self.animateLerp(percentage)
