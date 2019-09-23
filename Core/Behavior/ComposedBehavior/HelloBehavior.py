from colour import Color
from Core.Enumerations import *
from Core.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Core.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseInOut import BlinkBehaviorEaseInOut

class HelloBehavior(ComposedBehavior):
    def __init__(self, controlRef):
        ComposedBehavior.__init__(self, controlRef)
        self.behaviorList.append(BlinkBehaviorEaseInOut(controlRef, [Color(rgb=(1.0, 1.0, 1.0))], ColorBrightness.MEDIUM, 3, 2.0, Color(rgb=(0.0, 0.0, 0.0))))