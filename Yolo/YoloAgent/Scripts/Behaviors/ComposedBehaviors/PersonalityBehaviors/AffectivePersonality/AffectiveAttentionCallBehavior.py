from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AffectiveAttentionCallBehavior(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.AFFECTIVE_ATTENTION_CALL

        return

    def prepareBehavior(self, body):

        for behavior in self.behaviorList:

                if behavior.behaviorType == Behaviors.BLINK:
                    behavior.prepareBehavior(body, [Color(rgb=(1.0, 1.0, 0.0))], ColorBrightness.HIGH, Transitions.EASEIN, 1, 1, body.getColor(), True)
                    pass
                elif behavior.behaviorType == Behaviors.FEELER:
                    pass
                elif behavior.behaviorType == Behaviors.MOVE:
                    behavior.prepareBehavior(body, Shapes.CIRCLE, 70, MovementDirection.STANDARD, Transitions.LINEAR, 3, 10, True)
                    pass
                else:
                    raise IndexError("Prepare behavior: This standard behavior type doesn't exist")

        return
