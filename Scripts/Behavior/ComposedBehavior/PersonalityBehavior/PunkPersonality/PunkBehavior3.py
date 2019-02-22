from colour import Color
from Libs.Constants import *
from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorInstant import BlinkBehaviorInstant

class PunkBehavior3(ComposedBehavior):
    def __init__(self, bodyRef):
        ComposedBehavior.__init__(self, bodyRef)
        self.behaviorType = ComposedBehaviorType.PUNK_EXPRESSION_3
        self.behaviorList.append(BlinkBehaviorInstant(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 2.5, Color(rgb=(0.0, 0.0, 0.0)), False))