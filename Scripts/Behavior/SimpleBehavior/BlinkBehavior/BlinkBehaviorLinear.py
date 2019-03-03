import time
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorLinear(BlinkBehavior):
	def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
	    BlinkBehavior.__init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor)
	    
	def behaviorActions(self):
	    BlinkBehavior.behaviorActions(self)
	    percentage = (time.time() - self.startTime) / self.behaviorDuration
	    self.animateLerp(percentage)