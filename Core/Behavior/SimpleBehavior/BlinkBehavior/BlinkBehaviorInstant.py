import time
from Core.Enumerations import *
from Core.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorInstant(BlinkBehavior, object):
	def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
	    super(BlinkBehaviorInstant, self).__init__(bodyRef, blinkColor, brightness, repetitions, duration, defaultColor)
	    
	def behaviorActions(self):
		super(BlinkBehaviorInstant, self).behaviorActions()
		self.bodyRef.setColor(self.blinkColor)
		self.bodyRef.setBrightness(self.brightness)

		# force insta blink
		timeElapsed = time.time() - self.startTime
		if(self.duration - timeElapsed < 0.1 * self.duration):
			self.bodyRef.setColor(self.defaultColor)
		

	def finishBehavior(self):
		super(BlinkBehaviorInstant, self).finishBehavior()
		self.bodyRef.setColor(self.defaultColor)

	def resetBehavior(self):
		super(BlinkBehaviorInstant, self).resetBehavior()
		self.bodyRef.setColor(self.defaultColor)
