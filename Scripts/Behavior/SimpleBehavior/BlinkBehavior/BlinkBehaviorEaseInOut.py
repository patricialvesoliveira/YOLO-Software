import time
from colour import Color
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseOut import BlinkBehaviorEaseOut

class BlinkBehaviorEaseInOut(BlinkBehavior, object):
    def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
        super(BlinkBehaviorEaseInOut, self).__init__(bodyRef, blinkColor, brightness, repetitions, duration, defaultColor)
        self.subBehaviorDuration = duration/ 2.0

        self.easeInBehavior = BlinkBehaviorEaseIn(self.bodyRef, self.blinkColor, self.brightness, 1, self.subBehaviorDuration, self.defaultColor)
        self.easeOutBehavior = BlinkBehaviorEaseOut(self.bodyRef, self.blinkColor, self.brightness, 1, self.subBehaviorDuration, self.defaultColor)
        
        self.resetBehaviors()

    def behaviorActions(self):
        super(BlinkBehaviorEaseInOut, self).behaviorActions()
        if not self.easeInBehavior.isOver:
            if(not self.behaviorInSet):
                self.easeInBehavior.resetBehavior()
                self.behaviorInSet = True
            self.easeInBehavior.behaviorActions()
        elif not self.easeOutBehavior.isOver:
            if(not self.behaviorOutSet):
                self.easeOutBehavior.resetBehavior()
                self.behaviorOutSet = True
            self.easeOutBehavior.behaviorActions()
        else:
            self.resetBehaviors()

    def resetBehaviors(self):
        self.easeInBehavior.resetBehavior()
        self.easeOutBehavior.resetBehavior()
        self.behaviorInSet = False
        self.behaviorOutSet = False
