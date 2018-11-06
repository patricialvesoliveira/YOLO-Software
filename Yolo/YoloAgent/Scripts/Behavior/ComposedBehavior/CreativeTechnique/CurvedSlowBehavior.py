from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorCurved import MoveBehaviorCurved
from Libs.Constants import *
import time


class CurvedSlowBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.CURVED_SLOW
        self.behaviorList.append(MoveBehaviorCurved(bodyRef, 45, MovementDirection.STANDARD, 1, 10, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)