from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AffectiveBehavior1(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.AFFECTIVE_EXPRESSION_1
        self.behaviorList.append(BlinkBehaviorEaseIn(body, [Color(rgb=(0.7, 0.0, 0.7))], ColorBrightness.MEDIUM, 1, 10, body.getColor(), True))