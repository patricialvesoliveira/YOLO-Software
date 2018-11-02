from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class PunkBehavior2(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.PUNK_EXPRESSION_2
        self.behaviorList.append(BlinkBehaviorEaseInOut(body, [Color(rgb=(1.0, 0.5, 0.0)), Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 10, body.getColor(), True))