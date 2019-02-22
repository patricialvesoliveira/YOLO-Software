import time
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorInstant(BlinkBehavior):
	def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
	    BlinkBehavior.__init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting, startDelay, animationPause)
	    
	def behaviorActions(self):
	    BlinkBehavior.behaviorActions(self)
	    self.bodyRef.setColor(self.activeBlinkColor)
	    self.bodyRef.setBrightness(self.activeBlinkBrightness)