from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class PunkIdleBehavior(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.PUNK_IDLE
        self.behaviorList.append(BlinkBehaviorEaseInOut(body, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.LOW, 1, 10, Color(rgb=(0.0, 0.0, 0.0)), True))