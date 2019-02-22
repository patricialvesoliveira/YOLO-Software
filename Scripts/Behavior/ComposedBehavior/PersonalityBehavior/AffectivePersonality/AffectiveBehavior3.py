from colour import Color
from Libs.Constants import *
from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn

class AffectiveBehavior3(ComposedBehavior):
    def __init__(self, bodyRef):
        ComposedBehavior.__init__(self, bodyRef)
        self.behaviorType = ComposedBehaviorType.AFFECTIVE_EXPRESSION_3
        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(1.0, 0.25, 0.0))], ColorBrightness.MEDIUM, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))
