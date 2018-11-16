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
        self.behaviorList.append(MoveBehaviorCurved(bodyRef, 30, MovementDirection.FORWARD, 2, 3.5, True))