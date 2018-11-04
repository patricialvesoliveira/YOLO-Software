import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import BlinkBehavior


class BlinkBehaviorLinear(BlinkBehavior):
	# Body body, int repetitions, float duration
	def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
	    BlinkBehavior.__init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting, startDelay, animationPause)
	    
	# Body body
	def applyBehavior(self):
	    BlinkBehavior.applyBehavior(self)
	    percentage = (time.time() - self._startTime) / self.animationIntervalTime
	    self.animateLerp(percentage)