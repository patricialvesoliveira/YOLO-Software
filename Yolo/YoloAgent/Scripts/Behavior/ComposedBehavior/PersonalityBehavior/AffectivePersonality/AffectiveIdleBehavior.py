from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseInOut import BlinkBehaviorEaseInOut
from colour import Color
from Libs.Constants import *
import time


class AffectiveIdleBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.AFFECTIVE_IDLE
        self.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.55, 0.0))], ColorBrightness.MEDIUM, 1, 2.0, Color(rgb=(0.0, 0.0, 0.0)), False))