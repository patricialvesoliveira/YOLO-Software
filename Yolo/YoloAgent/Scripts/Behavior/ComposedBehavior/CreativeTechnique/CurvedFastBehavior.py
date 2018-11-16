from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorCurved import MoveBehaviorCurved
from Libs.Constants import *
import time


class CurvedFastBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.CURVED_FAST
        self.behaviorList.append(MoveBehaviorCurved(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
