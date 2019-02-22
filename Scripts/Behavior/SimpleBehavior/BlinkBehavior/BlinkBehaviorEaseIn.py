import time
import numpy
from colour import Color
import pytweening as tween
from Libs.Constants import *
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorEaseIn(BlinkBehavior):
    def __init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting=False, startDelay = 0.0, animationPause = 0.0):
        BlinkBehavior.__init__(self, bodyRef, blinkColorList, brightness, repetitions, duration, defaultColor, keepBehaviorSetting, startDelay, animationPause)
    
    def behaviorActions(self):
        BlinkBehavior.behaviorActions(self)
        timeElapsed = time.time() - self.startTime
        percentage = tween.easeInSine(numpy.clip(timeElapsed / self.duration, 0, 1))
        self.animateLerp(percentage)