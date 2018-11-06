from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorLoops import MoveBehaviorLoops
from Libs.Constants import *
import time


class LoopsSlowBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.LOOPS_SLOW
        self.behaviorList.append(MoveBehaviorLoops(bodyRef, 45, MovementDirection.STANDARD, 1, 5, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)