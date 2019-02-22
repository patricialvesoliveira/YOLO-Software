from colour import Color
from Libs.Constants import *
from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseIn import BlinkBehaviorEaseIn
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorCircle import MoveBehaviorCircle

class AffectiveAttentionCallBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        ComposedBehavior.__init__(self, bodyRef)
        self.behaviorType = ComposedBehaviorType.AFFECTIVE_ATTENTION_CALL
        self.behaviorList.append(BlinkBehaviorEaseIn(bodyRef, [Color(rgb=(1.0, 0.25, 0.0))], ColorBrightness.MEDIUM, 1.0, 1.0, Color(rgb=(0.0, 0.0, 0.0)), True))
        self.behaviorList.append(MoveBehaviorCircle(bodyRef, 40.0, MovementDirection.FORWARD, 3.0, 5.0, True))