from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from colour import Color
from Libs.Constants import *
import time


class PuppeteerBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.PUPPETEER
        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(1.0, 1.0, 0.0))], ColorBrightness.HIGH, 1, 1, bodyRef.getColor(), True))