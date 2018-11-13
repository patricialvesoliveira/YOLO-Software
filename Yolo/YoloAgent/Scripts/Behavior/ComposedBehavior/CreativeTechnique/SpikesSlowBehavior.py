from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorSpikes import MoveBehaviorSpikes
from Libs.Constants import *
import time


class SpikesSlowBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.SPIKES_SLOW
        self.behaviorList.append(MoveBehaviorSpikes(bodyRef, 45, MovementDirection.STANDARD, 1, 5, 2, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)