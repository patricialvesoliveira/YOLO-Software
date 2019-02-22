from Libs.Constants import *
from colour import Color
from Scripts.Behavior.ComposedBehavior.ComposedBehavior import ComposedBehavior
from Scripts.Behavior.SimpleBehavior.MoveBehavior.MoveBehaviorRect import MoveBehaviorRect
from Scripts.Behavior.SimpleBehavior.BlinkBehavior.BlinkBehaviorEaseInOut import BlinkBehaviorEaseInOut


class RectFastBehavior(ComposedBehavior):
    def __init__(self, bodyRef):
        # standard behaviors
        ComposedBehavior.__init__(self, bodyRef)

        # generic variables
        self.behaviorType = ComposedBehaviorType.RECT_FAST
        self.behaviorList.append(MoveBehaviorRect(bodyRef, 95, MovementDirection.FORWARD, 2, 1.5, True))
        self.behaviorList.append(BlinkBehaviorEaseInOut(bodyRef, [bodyRef.getStimulusColor()], ColorBrightness.HIGH, 1, 3.0, Color(rgb=(0.0, 0.0, 0.0)), False))