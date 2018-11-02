from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from colour import Color
from Libs.Constants import *
import time


class AloofBehavior1(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.ALOOF_EXPRESSION_1
        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(0.0, 1.0, 0.0))], ColorBrightness.MEDIUM, 1, 10, Color(rgb=(0.0, 0.0, 0.0)), True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)