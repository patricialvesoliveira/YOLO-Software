from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorLoops import MoveBehaviorLoops
from Libs.Constants import *
import time


class LoopsFastBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.LOOPS_FAST
        self.behaviorList.append(MoveBehaviorLoops(bodyRef, 60, MovementDirection.STANDARD, 2, 7, 2, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)
