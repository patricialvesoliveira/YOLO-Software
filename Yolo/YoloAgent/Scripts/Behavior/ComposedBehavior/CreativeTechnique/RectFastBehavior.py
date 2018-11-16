from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorRect import MoveBehaviorRect
from Libs.Constants import *
import time


class RectFastBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.RECT_FAST
        self.behaviorList.append(MoveBehaviorRect(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))