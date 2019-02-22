from colour import Color
from Libs.Constants import *
from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseInOut import BlinkBehaviorEaseInOut
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorLoops import MoveBehaviorLoops

class PunkBehavior2(ComposedBehavior):
    def __init__(self, bodyRef):
        ComposedBehavior.__init__(self, bodyRef)
        self.behaviorType = ComposedBehaviorType.PUNK_EXPRESSION_2
        self.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [Color(rgb=(1.0, 0.0, 0.0))], ColorBrightness.HIGH, 1, 4.5, Color(rgb=(0.0, 0.0, 0.0)), False))
        self.behaviorList.append(MoveBehaviorLoops(bodyRef, 80, MovementDirection.FORWARD, 3, 1.5, False))