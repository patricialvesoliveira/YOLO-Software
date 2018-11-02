from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AffectiveAttentionCallBehavior(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.AFFECTIVE_ATTENTION_CALL
        self.behaviorList.append(BlinkBehaviorEaseIn(body, [Color(rgb=(1.0, 1.0, 0.0))], ColorBrightness.HIGH, 1, 1, body.getColor(), True))
        self.behaviorList.append(MoveBehavior(body, Shapes.CIRCLE, 70, MovementDirection.STANDARD, Transitions.LINEAR, 3, 10, True))