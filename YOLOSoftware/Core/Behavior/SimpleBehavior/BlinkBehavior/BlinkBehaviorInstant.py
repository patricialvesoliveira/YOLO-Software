import time
from Libs.Constants import *
from Core.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorInstant(BlinkBehavior, object):
	def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
	    super(BlinkBehaviorInstant, self).__init__(bodyRef, blinkColor, brightness, repetitions, duration, defaultColor)
	    
	def behaviorActions(self):
		super(BlinkBehaviorInstant, self).behaviorActions()
		self.bodyRef.setColor(self.blinkColor)
		self.bodyRef.setBrightness(self.brightness)