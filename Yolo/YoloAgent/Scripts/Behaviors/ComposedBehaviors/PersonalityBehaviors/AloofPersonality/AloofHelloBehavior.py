from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AloofHelloBehavior(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.ALOOF_HELLO
        self.behaviorList.append(BlinkBehaviorEaseInOut(body, [Color(rgb=(0.0, 0.0, 1.0))], ColorBrightness.HIGH, 3, 6, Color(rgb=(0.0, 0.0, 0.0)), False))