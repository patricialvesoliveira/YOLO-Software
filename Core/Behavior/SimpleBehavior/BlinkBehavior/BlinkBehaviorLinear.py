import time
from Core.Enumerations import *
from Core.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorLinear(BlinkBehavior, object):
	def __init__(self, controlRef, blinkColor, brightness, repetitions, duration, defaultColor):
	    super(BlinkBehaviorLinear, self).__init__(controlRef, blinkColor, brightness, repetitions, duration, defaultColor)
	    
	def behaviorActions(self):
	    super(BlinkBehaviorLinear, self).behaviorActions()
	    percentage = (time.time() - self.startTime) / self.duration
	    self.animateLerp(percentage)