import time
from Libs.Constants import *
from YOLOSoftware.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorLinear(BlinkBehavior, object):
	def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
	    super(BlinkBehaviorLinear, self).__init__(bodyRef, blinkColor, brightness, repetitions, duration, defaultColor)
	    
	def behaviorActions(self):
	    super(BlinkBehaviorLinear, self).behaviorActions()
	    percentage = (time.time() - self.startTime) / self.behaviorDuration
	    self.animateLerp(percentage)