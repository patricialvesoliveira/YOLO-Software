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

        self.subBehaviorDuration = duration/ 2.0
        self.resetBehaviors()


    def behaviorActions(self):
        BlinkBehavior.behaviorActions(self)

        # print "isOver1: "+ str(self.easeInBehavior.isOver)
        # print "isOver2: "+ str(self.easeOutBehavior.isOver)
        if not self.easeInBehavior.isOver:
            self.easeInBehavior.behaviorActions()

        elif not self.easeOutBehavior.isOver:
            if(not self.behaviorOutSet):
                self.easeOutBehavior = BlinkBehaviorEaseOut(self.bodyRef, self.blinkColorList, self.brightness, 1, self.subBehaviorDuration, self.defaultColor, False)
                self.behaviorOutSet = True
            self.easeOutBehavior.behaviorActions()
            
        # print self.currentBehaviorRepetition
        # print self.maxBehaviorRepetitions
        if self.checkForBehaviorEnd():
            self.resetBehaviors()
                     
        return

    def resetBehaviors(self):
        self.easeInBehavior = BlinkBehaviorEaseIn(self.bodyRef, self.blinkColorList, self.brightness, 1, self.subBehaviorDuration, self.defaultColor, False)
        self.easeOutBehavior = BlinkBehaviorEaseOut(self.bodyRef, self.blinkColorList, self.brightness, 1, self.subBehaviorDuration, self.defaultColor, False)
 
        self.behaviorInSet = True
        self.behaviorOutSet = False
