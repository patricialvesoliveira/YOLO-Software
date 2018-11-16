from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorStraight import MoveBehaviorStraight
from Libs.Constants import *
import time


class StraightFastBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.STRAIGHT_FAST
        self.behaviorList.append(MoveBehaviorStraight(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))