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

        self.subBehaviorDuration = duration / 2

        self.easeInBehavior = BlinkBehaviorEaseIn(bodyRef, blinkColorList, brightness, 1, self.subBehaviorDuration, defaultColor, True)
        self.easeOutBehavior = BlinkBehaviorEaseOut(bodyRef, blinkColorList, brightness, 1, self.subBehaviorDuration, defaultColor, False)
        
    def behaviorActions(self):
        BlinkBehavior.behaviorActions(self)

        if not self.easeInBehavior.isOver:
            self.easeInBehavior.behaviorActions()
        elif not self.easeOutBehavior.isOver:
            self.easeOutBehavior.behaviorActions()
        elif self.currentBehaviorRepetition==0 or self.currentBehaviorRepetition <= self.maxBehaviorRepetitions: #reset ease in and ease out
            self.easeInBehavior = BlinkBehaviorEaseIn(self.bodyRef, self.blinkColorList, self.brightness, 1, self.subBehaviorDuration, self.defaultColor, True)
            self.easeOutBehavior = BlinkBehaviorEaseOut(self.bodyRef, self.blinkColorList, self.brightness, 1, self.subBehaviorDuration, self.defaultColor, False)
               
        return