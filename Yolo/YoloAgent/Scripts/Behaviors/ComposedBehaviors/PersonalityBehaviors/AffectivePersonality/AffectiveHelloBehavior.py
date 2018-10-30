from Scripts.Behaviors.ComposedBehaviors.ComposedBehavior import ComposedBehavior
from Scripts.Behaviors.SimpleBehaviors.BlinkBehavior import *
from Scripts.Behaviors.SimpleBehaviors.FeelerBehavior import *
from Scripts.Behaviors.SimpleBehaviors.MoveBehavior import *
from Libs.Constants import *
import time


class AffectiveHelloBehavior(ComposedBehavior):
    def __init__(self):
        # standard behaviors
        ComposedBehavior.__init__(self)

        # generic variables
        self.behaviorType = ComposedBehaviors.AFFECTIVE_HELLO

        return

    def prepareBehavior(self, body):

        for behavior in self.behaviorList:

                if behavior.behaviorType == Behaviors.BLINK:
                    behavior.prepareBehavior(body, [Color(rgb=(1.0, 1.0, 0.0))], ColorBrightness.HIGH, Transitions.EASEINOUT, 3, 6, Color(rgb=(0.0, 0.0, 0.0)), False)
                    pass
                elif behavior.behaviorType == Behaviors.FEELER:
                    behavior.prepareBehavior(body, 50, Transitions.LINEAR, 1, 5, True)
                    pass
                elif behavior.behaviorType == Behaviors.MOVE:
                    #behavior.prepareBehavior(body, Shapes.CURVED, 70, MovementDirection.ALTERNATING, Transitions.LINEAR, 4, 8, True)
                    pass
                else:
                    raise IndexError("Prepare behavior: This standard behavior type doesn't exist")

        return
