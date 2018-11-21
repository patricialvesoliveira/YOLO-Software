from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseInOut import BlinkBehaviorEaseInOut
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorStraight import MoveBehaviorStraight
from colour import Color
from Libs.Constants import *
import time


class AloofBehavior3(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.ALOOF_EXPRESSION_3
        self.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(0.0, 0.0, 0.1))], ColorBrightness.LOW, 1, 8.0, Color(rgb=(0.0, 0.0, 0.0)), False))