from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorCurved import MoveBehaviorCurved
from Libs.Constants import *
from colour import Color
import time


class AffectiveBehavior1(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.AFFECTIVE_EXPRESSION_1
        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(1.0, 0.25, 0.0))], ColorBrightness.MEDIUM, 1.0, 1.0, Color(rgb=(0.0, 0.0, 0.0)), False))
        self.behaviorList.append(MoveBehaviorCurved(bodyRef, 40.0, MovementDirection.FORWARD, 2, 6.0, False))