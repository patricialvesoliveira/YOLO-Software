from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorStraight import MoveBehaviorStraight
from colour import Color
from Libs.Constants import *
import time


class PunkAttentionCallBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.PUNK_ATTENTION_CALL

        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 10, bodyRef.getColor(), True))
        self.behaviorList.append(MoveBehaviorStraight(bodyRef, 70, MovementDirection.ALTERNATING, 3, 10, 2, True))