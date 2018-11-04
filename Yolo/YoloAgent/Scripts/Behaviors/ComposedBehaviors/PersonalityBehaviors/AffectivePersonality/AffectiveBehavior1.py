from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
from colour import Color
import time


class AffectiveBehavior1(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.AFFECTIVE_EXPRESSION_1
        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(0.7, 0.0, 0.7))], ColorBrightness.MEDIUM, 1, 10, bodyRef.getColor(), True))
