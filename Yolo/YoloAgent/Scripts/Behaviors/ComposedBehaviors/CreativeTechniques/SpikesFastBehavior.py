from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class SpikesFastBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.SPIKES_FAST
        self.behaviorList.append(MoveBehavior(bodyRef, Shapes.SPIKES, 60, MovementDirection.STANDARD, Transitions.LINEAR, 2, 7, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)