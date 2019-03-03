import time
from colour import Color
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn

class BlinkBehaviorEaseOut(BlinkBehaviorEaseIn, object):
    def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
    	#an ease out is an ease to black 
    	super(BlinkBehaviorEaseOut, self).__init__(bodyRef, Color(rgb=(0.0, 0.0, 0.0)), brightness, repetitions, duration, defaultColor)
    	self.bodyColorAtStart = blinkColor
    	self.isBodyColorSet = False
