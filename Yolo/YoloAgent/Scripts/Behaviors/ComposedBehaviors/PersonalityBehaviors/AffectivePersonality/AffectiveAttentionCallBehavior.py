from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
from colour import Color
import time


class AffectiveAttentionCallBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.AFFECTIVE_ATTENTION_CALL
        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(1.0, 1.0, 0.0))], ColorBrightness.HIGH, 1, 1, bodyRef.getColor(), True))
        self.behaviorList.append(MoveBehavior(bodyRef, Shapes.CIRCLE, 70, MovementDirection.STANDARD, Transitions.LINEAR, 3, 10, True))