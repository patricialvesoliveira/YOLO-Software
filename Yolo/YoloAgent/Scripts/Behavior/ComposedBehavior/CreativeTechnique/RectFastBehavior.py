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
        self.behaviorList.append(MoveBehaviorRect(bodyRef, 60, MovementDirection.STANDARD, 1, 7, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)