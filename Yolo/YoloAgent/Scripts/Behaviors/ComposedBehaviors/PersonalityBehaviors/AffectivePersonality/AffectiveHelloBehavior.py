from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior.BlinkBehaviorEaseInOut import BlinkBehaviorEaseInOut
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
from colour import Color
import time

class AffectiveHelloBehavior(ComposedBehavior):
    def __init__(self, bodyRef):

        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviors.AFFECTIVE_HELLO
        self.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 1.0, 0.0))], ColorBrightness.HIGH, 3, 12, Color(rgb=(0.0, 0.0, 0.0)), False))