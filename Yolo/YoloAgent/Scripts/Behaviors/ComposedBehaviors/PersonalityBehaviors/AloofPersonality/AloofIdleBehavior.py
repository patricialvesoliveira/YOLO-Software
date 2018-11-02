from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AloofIdleBehavior(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.ALOOF_IDLE
        self.behaviorList.append(BlinkBehaviorEaseInOut(body, [Color(rgb=(0.0, 0.0, 1.0))], ColorBrightness.LOW, 1, 12, Color(rgb=(0.0, 0.0, 0.0)), False))