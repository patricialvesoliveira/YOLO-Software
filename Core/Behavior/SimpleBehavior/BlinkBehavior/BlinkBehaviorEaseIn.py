import time
import numpy
from colour import Color
import pytweening as tween
from Core.Enumerations import *
from Core.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehavior import BlinkBehavior

class BlinkBehaviorEaseIn(BlinkBehavior, object):
    def __init__(self, controlRef, blinkColor, brightness, repetitions, duration, defaultColor):
        super(BlinkBehaviorEaseIn, self).__init__(controlRef, blinkColor, brightness, repetitions, duration, defaultColor)
    
    def behaviorActions(self):
        super(BlinkBehaviorEaseIn, self).behaviorActions()
        timeElapsed = time.time() - self.startTime
        percentage = tween.easeInSine(numpy.clip(timeElapsed / self.duration, 0, 1))
        self.controlRef.setColor(self.lerpColor(percentage, self.controlColorAtStart, self.blinkColor))
        self.controlRef.setBrightness(self.brightness * percentage + self.controlBrightnessAtStart * (1 - percentage))