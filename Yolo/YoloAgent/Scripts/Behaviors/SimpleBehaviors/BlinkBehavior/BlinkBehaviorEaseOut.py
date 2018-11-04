import sys
import time
import numpy

from colour import Color
import pytweening as tween

from Libs.Constants import *
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import BlinkBehavior


class BlinkBehaviorEaseOut(BlinkBehavior):
	# Body body, int repetitions, float duration
	def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
	    BlinkBehavior.__init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting, startDelay, animationPause)

	# Body body
	def applyBehavior(self):
	    BlinkBehavior.applyBehavior(self)
	    timeElapsed = time.time() - self.startTime
	    percentage = tween.easeOutSine(numpy.clip(timeElapsed / self.animationIntervalTime, 0, 1))
	    self.animateLerp(percentage)