from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorSpikes import MoveBehaviorSpikes
from Libs.Constants import *
import time


class SpikesFastBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.SPIKES_FAST
        self.behaviorList.append(MoveBehaviorSpikes(bodyRef, 60, MovementDirection.STANDARD, 2, 7, 2, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)