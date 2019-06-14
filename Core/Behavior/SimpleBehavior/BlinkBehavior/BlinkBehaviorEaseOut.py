import time
from colour import Color
from Core.Enumerations import *
from Core.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior
from Core.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn

class BlinkBehaviorEaseOut(BlinkBehavior, object):
    def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
    	super(BlinkBehaviorEaseOut, self).__init__(bodyRef, blinkColor, brightness, repetitions, duration, defaultColor)
    	#an ease out is an ease to black 
    	self.easeInBehavior = BlinkBehaviorEaseIn(bodyRef, Color(rgb=(0.0, 0.0, 0.0)), brightness, repetitions, duration, defaultColor)
    	self.easeInBehavior.bodyColorAtStart = blinkColor

    def behaviorActions(self):
        super(BlinkBehaviorEaseOut, self).behaviorActions()
    	self.easeInBehavior.behaviorActions()

    def finishBehavior(self):
        super(BlinkBehaviorEaseOut, self).finishBehavior()
        self.easeInBehavior.resetBehavior()

    def resetBehavior(self):
        super(BlinkBehaviorEaseOut, self).resetBehavior()
    	self.easeInBehavior.resetBehavior()
