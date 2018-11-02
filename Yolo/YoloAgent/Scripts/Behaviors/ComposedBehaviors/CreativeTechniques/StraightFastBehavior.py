from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class StraightFastBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.STRAIGHT_FAST
        self.behaviorList.append(MoveBehavior(bodyRef, Shapes.STRAIGHT, 60, MovementDirection.STANDARD, Transitions.LINEAR, 1, 5, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)