from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorStraight import MoveBehaviorStraight
from Libs.Constants import *
import time


class StraightSlowBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.STRAIGHT_SLOW
        self.behaviorList.append(MoveBehaviorStraight(bodyRef, 45, MovementDirection.STANDARD, 1, 5, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)