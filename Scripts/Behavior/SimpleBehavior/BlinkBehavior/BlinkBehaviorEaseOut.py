import time
from colour import Color
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn

class BlinkBehaviorEaseOut(BlinkBehaviorEaseIn):
    def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
    	#an ease out is an ease to black 
        BlinkBehaviorEaseIn.__init__(self, bodyRef, [Color(rgb=(0.0, 0.0, 0.0))], brightness, repetitions, duration, defaultColor, keepBehaviorSetting, startDelay, animationPause)