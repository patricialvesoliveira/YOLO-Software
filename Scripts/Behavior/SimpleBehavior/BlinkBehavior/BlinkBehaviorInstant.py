import time
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorInstant(BlinkBehavior):
	def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
	    BlinkBehavior.__init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor)
	    
	def behaviorActions(self):
	    BlinkBehavior.behaviorActions(self)
	    self.bodyRef.setColor(self.activeBlinkColor)
	    self.bodyRef.setBrightness(self.activeBlinkBrightness)