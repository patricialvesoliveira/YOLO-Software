import time
from colour import Color
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn

class BlinkBehaviorEaseOut(BlinkBehaviorEaseIn):
    def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
    	#an ease out is an ease to black 
    	bodyRef.setColor(blinkColor)
        BlinkBehaviorEaseIn.__init__(self, bodyRef, Color(rgb=(0.0, 0.0, 0.0)), brightness, repetitions, duration, defaultColor)