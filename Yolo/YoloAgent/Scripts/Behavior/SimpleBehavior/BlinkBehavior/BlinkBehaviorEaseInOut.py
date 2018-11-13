import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseOut import BlinkBehaviorEaseOut


class BlinkBehaviorEaseInOut(BlinkBehavior):
    # Body body, int repetitions, float duration
    def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
        BlinkBehavior.__init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, False, startDelay, animationPause)

        subBehaviorDuration = duration / 2

        self.easeInBehavior = BlinkBehaviorEaseIn(bodyRef, blinkColorList, brightness, 1, subBehaviorDuration, defaultColor)
        self.easeOutBehavior = BlinkBehaviorEaseOut(bodyRef, blinkColorList, brightness, 1, subBehaviorDuration, defaultColor)
        

    # Body body
    def applyBehavior(self):
        BlinkBehavior.applyBehavior(self)

        if not self.easeInBehavior.isOver:
            self.easeInBehavior.applyBehavior()
        else:
            self.easeOutBehavior.applyBehavior()
