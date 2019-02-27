from colour import Color
from Libs.Constants import *
from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorInstant import BlinkBehaviorInstant
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorSpikes import MoveBehaviorSpikes

class PuppeteerBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.PUPPETEER
        self.behaviorList.append(BlinkBehaviorInstant(bodyRef, [Color(rgb=(1.0, 1.0, 1.0))], ColorBrightness.HIGH, 0, 1.0, bodyRef.getColor(), False))