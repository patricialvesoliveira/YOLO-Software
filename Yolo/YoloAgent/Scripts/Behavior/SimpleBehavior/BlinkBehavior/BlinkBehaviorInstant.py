import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior


class BlinkBehaviorInstant(BlinkBehavior):
	# Body body, int repetitions, float duration
	def __init__(self, bodyRef, blinkColorList, brightness, repetitions, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
	    BlinkBehavior.__init__(self, bodyRef, blinkColorList, brightness, repetitions, 0.5, defaultColor, keepBehaviorSetting, startDelay, animationPause)
	    
	# Body body
	def applyBehavior(self):
	    BlinkBehavior.applyBehavior(self)
	    self.bodyRef.setColor(self.activeBlinkColor)