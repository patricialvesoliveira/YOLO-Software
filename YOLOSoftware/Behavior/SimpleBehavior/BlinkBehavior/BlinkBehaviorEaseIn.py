import time
import numpy
from colour import Color
import pytweening as tween
from Libs.Constants import *
from YOLOSoftware.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorEaseIn(BlinkBehavior, object):
    def __init__(self, bodyRef, blinkColor, brightness, repetitions, duration, defaultColor):
        super(BlinkBehaviorEaseIn, self).__init__(bodyRef, blinkColor, brightness, repetitions, duration, defaultColor)
    
    def behaviorActions(self):
        super(BlinkBehaviorEaseIn, self).behaviorActions()
        timeElapsed = time.time() - self.startTime
        percentage = tween.easeInSine(numpy.clip(timeElapsed / self.duration, 0, 1))
        self.bodyRef.setColor(self.lerpColor(percentage, self.bodyColorAtStart, self.blinkColor))
        self.bodyRef.setBrightness(self.brightness * percentage + self.bodyBrightnessAtStart * (1 - percentage))