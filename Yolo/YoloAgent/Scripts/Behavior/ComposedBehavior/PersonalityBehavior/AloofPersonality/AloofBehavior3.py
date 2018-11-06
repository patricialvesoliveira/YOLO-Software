from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from colour import Color
from Libs.Constants import *
import time


class AloofBehavior3(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.ALOOF_EXPRESSION_3
        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(0.0, 0.0, 0.0))], ColorBrightness.MEDIUM, 1, 7, Color(rgb=(0.0, 0.0, 0.0)), True))