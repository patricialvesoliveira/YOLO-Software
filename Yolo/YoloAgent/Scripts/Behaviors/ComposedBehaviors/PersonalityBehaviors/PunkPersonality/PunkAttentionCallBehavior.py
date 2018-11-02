from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from colour import Color
from Libs.Constants import *
import time


class PunkAttentionCallBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.PUNK_ATTENTION_CALL

        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 10, bodyRef.getColor(), True))
        self.behaviorList.append(MoveBehavior(bodyRef, Shapes.STRAIGHT, 70, MovementDirection.ALTERNATING, Transitions.LINEAR, 3, 10, True))

    def applyBehavior(self):
        ComposedBehavior.applyBehavior(self)