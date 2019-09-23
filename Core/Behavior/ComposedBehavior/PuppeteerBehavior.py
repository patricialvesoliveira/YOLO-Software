from colour import Color
from Core.Enumerations import *
from Core.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Core.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorInstant import BlinkBehaviorInstant
from Core.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorSpikes import MoveBehaviorSpikes

class PuppeteerBehavior(ComposedBehavior):
    def __init__(self, controlRef):
        ComposedBehavior.__init__(self, controlRef)
        self.behaviorList.append(BlinkBehaviorInstant(controlRef, [Color(rgb=(1.0, 1.0, 1.0))], ColorBrightness.HIGH, 0, 1.0, controlRef.getColor()))