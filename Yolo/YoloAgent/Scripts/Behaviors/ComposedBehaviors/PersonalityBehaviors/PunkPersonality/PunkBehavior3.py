from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior.BlinkBehaviorEaseInOut import BlinkBehaviorEaseInOut
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from colour import Color
from Libs.Constants import *
import time


class PunkBehavior3(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.PUNK_EXPRESSION_3
        self.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.5, 0.0))], ColorBrightness.MEDIUM, 1, 10, Color(rgb=(0.0, 0.0, 0.0)), True))